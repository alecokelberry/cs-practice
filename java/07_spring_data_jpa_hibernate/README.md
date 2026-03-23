# 07 — Spring Data JPA & Hibernate

Spring Data JPA provides a repository abstraction over JPA (Java Persistence API). Hibernate is the JPA implementation that does the actual SQL generation. You write Java classes and method names; Hibernate writes SQL.

---

## The Stack

```
Your Code
    ↓
Spring Data JPA     — repository interfaces, query generation
    ↓
JPA (API)           — standard persistence spec
    ↓
Hibernate           — JPA implementation, generates SQL
    ↓
JDBC
    ↓
Database (PostgreSQL, MySQL, H2, etc.)
```

---

## Dependencies (`pom.xml`)

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

For development/testing, H2 is an in-memory database (no install needed):
```xml
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
</dependency>
```

---

## Mapping an Entity

An **entity** is a Java class mapped to a database table.

```java
@Entity
@Table(name = "users") // optional — defaults to class name
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // auto-increment
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    // JPA requires a no-arg constructor
    protected User() {}

    public User(String name, String email) {
        this.name = name;
        this.email = email;
        this.createdAt = LocalDateTime.now();
    }

    // getters and setters (or use @Data from Lombok)
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}
```

`@GeneratedValue` strategies:
| Strategy | Behavior |
|----------|----------|
| `IDENTITY` | Database auto-increment (PostgreSQL `SERIAL`, MySQL `AUTO_INCREMENT`) |
| `SEQUENCE` | Database sequence (default for PostgreSQL, preferred for performance) |
| `AUTO` | Hibernate picks based on database |

---

## `application.properties` for JPA

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=postgres
spring.datasource.password=secret

# DDL auto: validate | update | create | create-drop | none
# Use "validate" in production, "update" in development
spring.jpa.hibernate.ddl-auto=update

# Log the SQL Hibernate generates (helpful for debugging)
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```

---

## The Repository

`JpaRepository<Entity, IdType>` provides CRUD operations automatically:

```java
@Repository  // optional — detected by Spring Data automatically
public interface UserRepository extends JpaRepository<User, Long> {
    // JpaRepository already gives you:
    //   save(entity), findById(id), findAll(), deleteById(id),
    //   existsById(id), count(), saveAll(...), etc.
}
```

### Query Methods — Derived from Method Name

Spring Data generates SQL from method names following a naming convention:

```java
public interface UserRepository extends JpaRepository<User, Long> {
    // SELECT * FROM users WHERE email = ?
    Optional<User> findByEmail(String email);

    // SELECT * FROM users WHERE name = ? AND email = ?
    List<User> findByNameAndEmail(String name, String email);

    // SELECT * FROM users WHERE name LIKE ?
    List<User> findByNameContainingIgnoreCase(String keyword);

    // SELECT * FROM users WHERE created_at > ?
    List<User> findByCreatedAtAfter(LocalDateTime date);

    // SELECT COUNT(*) FROM users WHERE email = ?
    boolean existsByEmail(String email);

    // DELETE FROM users WHERE email = ?
    void deleteByEmail(String email);

    // SELECT * FROM users ORDER BY name ASC LIMIT ?
    List<User> findTop10ByOrderByNameAsc();
}
```

Keywords: `findBy`, `findAllBy`, `countBy`, `existsBy`, `deleteBy`, `And`, `Or`, `Containing`, `StartingWith`, `EndingWith`, `IgnoreCase`, `After`, `Before`, `Between`, `OrderBy`, `Top{N}`.

---

## Custom Queries with `@Query`

When method names get unwieldy, write JPQL (Java Persistence Query Language) directly. JPQL looks like SQL but operates on entity classes, not table names.

```java
public interface UserRepository extends JpaRepository<User, Long> {

    // JPQL — "User" is the class name, "u.email" is the field
    @Query("SELECT u FROM User u WHERE u.email = :email")
    Optional<User> findByEmailJpql(@Param("email") String email);

    // Native SQL — uses actual table/column names
    @Query(value = "SELECT * FROM users WHERE email = :email", nativeQuery = true)
    Optional<User> findByEmailNative(@Param("email") String email);

    // Modifying query — must be paired with @Transactional
    @Modifying
    @Transactional
    @Query("UPDATE User u SET u.name = :name WHERE u.id = :id")
    int updateName(@Param("id") Long id, @Param("name") String name);
}
```

---

## Relationships

### One-to-Many / Many-to-One

```java
@Entity
public class Post {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String title;

    // One post has many comments
    @OneToMany(mappedBy = "post", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Comment> comments = new ArrayList<>();
}

@Entity
public class Comment {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String content;

    // Many comments belong to one post
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "post_id") // the foreign key column
    private Post post;
}
```

`mappedBy = "post"` means: the `Post` side doesn't own the foreign key; the `Comment.post` field does.

`cascade = CascadeType.ALL` means: operations on `Post` (save, delete) cascade to its `Comment`s.

`orphanRemoval = true` means: removing a comment from `post.comments` also deletes it from the database.

### Many-to-Many

```java
@Entity
public class Student {
    @ManyToMany
    @JoinTable(
        name = "student_course",
        joinColumns = @JoinColumn(name = "student_id"),
        inverseJoinColumns = @JoinColumn(name = "course_id")
    )
    private Set<Course> courses = new HashSet<>();
}

@Entity
public class Course {
    @ManyToMany(mappedBy = "courses")
    private Set<Student> students = new HashSet<>();
}
```

---

## Fetch Types

| Strategy | When the related data loads | Use When |
|----------|----------------------------|----------|
| `LAZY` | On access (separate query) | Most cases — avoids loading unnecessary data |
| `EAGER` | Immediately with the parent | You always need the related data |

**Default:** `@ManyToOne` and `@OneToOne` are EAGER by default. `@OneToMany` and `@ManyToMany` are LAZY by default.

**Rule:** Always use `LAZY` unless you have a proven performance reason. EAGER loading in collections causes N+1 queries and performance disasters.

---

## The N+1 Problem

If you load 100 posts and each post lazily fetches its author, Hibernate runs 1 query for posts + 100 queries for authors = 101 queries. Fix with a JOIN FETCH:

```java
@Query("SELECT p FROM Post p JOIN FETCH p.author WHERE p.published = true")
List<Post> findPublishedWithAuthor();
```

Or use `@EntityGraph`:
```java
@EntityGraph(attributePaths = {"author"})
List<Post> findByPublishedTrue();
```

---

## `@Transactional`

Wraps a method in a database transaction. If the method throws a `RuntimeException`, the transaction rolls back.

```java
@Service
public class OrderService {
    private final OrderRepository orderRepo;
    private final InventoryRepository inventoryRepo;

    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        Order order = new Order(request.userId(), request.items());
        orderRepo.save(order);                         // part 1
        inventoryRepo.decrementStock(request.items()); // part 2 — rolls back both if this fails
        return order;
    }
}
```

Without `@Transactional`, a failure in part 2 would leave part 1 committed — an inconsistent state. With it, both succeed or both are rolled back.

**Rule:** Put `@Transactional` on service methods, not repository or controller methods.

---

## Pagination and Sorting

```java
// Controller
@GetMapping
public Page<UserDto> list(
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "20") int size
) {
    Pageable pageable = PageRequest.of(page, size, Sort.by("name").ascending());
    return userRepository.findAll(pageable).map(this::toDto);
}

// Custom paginated query
Page<User> findByNameContaining(String name, Pageable pageable);
```

---

## Common Pitfalls

**No-arg constructor missing**
JPA requires a no-arg constructor to instantiate entities. Make it `protected` so your code can't accidentally use it.

**`toString()` or `equals()` on lazy fields**
Calling `user.getOrders().toString()` outside a transaction will trigger lazy loading and throw `LazyInitializationException`. Only access lazy relationships inside a transactional context.

**`CascadeType.ALL` on `@ManyToMany`**
Cascading delete on a many-to-many relationship can accidentally delete shared entities. Use `CascadeType.PERSIST` and `CascadeType.MERGE` instead, never `REMOVE` on `@ManyToMany`.

---

## Quick Reference

```
Entity
  @Entity                       marks the class
  @Table(name = "t")            custom table name
  @Id                           primary key
  @GeneratedValue(strategy = GenerationType.IDENTITY)  auto-increment
  @Column(nullable=false, unique=true, name="col")

Repository
  extends JpaRepository<Entity, IdType>
  findById(id)                  Optional<T>
  findAll()                     List<T>
  save(entity)                  insert or update
  deleteById(id)
  existsByField(val)            derived query method

Relationships
  @OneToMany(mappedBy="field", cascade=CascadeType.ALL, orphanRemoval=true)
  @ManyToOne(fetch=FetchType.LAZY) @JoinColumn(name="fk_col")
  @ManyToMany @JoinTable(...)

Queries
  @Query("SELECT e FROM Entity e WHERE e.field = :p")  JPQL
  @Query(value="SELECT ...", nativeQuery=true)          SQL
  @Modifying @Transactional — required for UPDATE/DELETE @Query

Transactions
  @Transactional on service methods — rolls back on RuntimeException

Pagination
  PageRequest.of(page, size, Sort.by("field").ascending())
  repository.findAll(pageable)  → Page<T>
```
