# 06 — REST Controllers & Services

Spring Boot's web layer has two parts: **controllers** that receive HTTP requests and return responses, and **services** that contain the business logic. Keeping them separate makes the code testable and easier to reason about.

---

## The Layered Architecture

```
HTTP Request
    ↓
@RestController     — parse input, call service, format output
    ↓
@Service            — business logic, validation, orchestration
    ↓
@Repository         — database access (lesson 7)
    ↓
Database
```

The controller knows about HTTP. The service knows nothing about HTTP — it works with plain Java objects. This makes the service easy to test without a web server.

---

## `@RestController`

Combines `@Controller` + `@ResponseBody`. Every return value is automatically serialized to JSON (via Jackson, which Spring Boot auto-configures).

```java
@RestController
@RequestMapping("/api/users") // base path for all methods in this controller
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<UserDto> getAll() {
        return userService.findAll();
    }

    @GetMapping("/{id}")
    public UserDto getById(@PathVariable Long id) {
        return userService.findById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED) // returns 201 instead of 200
    public UserDto create(@RequestBody @Valid CreateUserRequest request) {
        return userService.create(request);
    }

    @PutMapping("/{id}")
    public UserDto update(@PathVariable Long id, @RequestBody @Valid UpdateUserRequest request) {
        return userService.update(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT) // returns 204
    public void delete(@PathVariable Long id) {
        userService.delete(id);
    }
}
```

---

## Request Mapping Annotations

| Annotation | HTTP Method | Typical Use |
|------------|------------|-------------|
| `@GetMapping` | GET | Retrieve resource(s) |
| `@PostMapping` | POST | Create a resource |
| `@PutMapping` | PUT | Replace a resource |
| `@PatchMapping` | PATCH | Partially update a resource |
| `@DeleteMapping` | DELETE | Remove a resource |
| `@RequestMapping` | Any | Base path or catch-all |

---

## Extracting Data from Requests

```java
// @PathVariable — from URL path segment /users/{id}
@GetMapping("/{id}")
public UserDto get(@PathVariable Long id) { ... }

// @RequestParam — from query string /users?page=2&size=10
@GetMapping
public Page<UserDto> list(
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "20") int size
) { ... }

// @RequestBody — from request body (JSON → Java object)
@PostMapping
public UserDto create(@RequestBody CreateUserRequest request) { ... }

// @RequestHeader — from HTTP header
@GetMapping("/me")
public UserDto getCurrentUser(@RequestHeader("Authorization") String token) { ... }
```

---

## `ResponseEntity`

`ResponseEntity` gives full control over the response: status code, headers, and body.

```java
@GetMapping("/{id}")
public ResponseEntity<UserDto> getById(@PathVariable Long id) {
    return userService.findById(id)
        .map(user -> ResponseEntity.ok(user))           // 200 OK
        .orElse(ResponseEntity.notFound().build());     // 404 Not Found
}

@PostMapping
public ResponseEntity<UserDto> create(@RequestBody CreateUserRequest request) {
    UserDto created = userService.create(request);
    URI location = URI.create("/api/users/" + created.id());
    return ResponseEntity.created(location).body(created); // 201 Created + Location header
}
```

---

## Validation with `@Valid`

Add `spring-boot-starter-validation` to your dependencies, then annotate the request class:

```java
public record CreateUserRequest(
    @NotBlank String name,
    @Email String email,
    @Min(18) int age
) {}

@PostMapping
public UserDto create(@RequestBody @Valid CreateUserRequest request) {
    // Spring validates before this runs — returns 400 if invalid
    return userService.create(request);
}
```

Common validation annotations:

| Annotation | Rule |
|------------|------|
| `@NotNull` | Not null |
| `@NotBlank` | Not null, not empty, not only whitespace |
| `@Email` | Valid email format |
| `@Min(n)` / `@Max(n)` | Number range |
| `@Size(min, max)` | String/collection length |
| `@Pattern(regexp)` | Regex match |

---

## The Service Layer

The service contains business logic. It knows nothing about HTTP.

```java
@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<UserDto> findAll() {
        return userRepository.findAll().stream()
            .map(this::toDto)
            .toList();
    }

    public Optional<UserDto> findById(Long id) {
        return userRepository.findById(id).map(this::toDto);
    }

    public UserDto create(CreateUserRequest request) {
        if (userRepository.existsByEmail(request.email())) {
            throw new DuplicateEmailException(request.email());
        }
        User user = new User(request.name(), request.email());
        return toDto(userRepository.save(user));
    }

    private UserDto toDto(User user) {
        return new UserDto(user.getId(), user.getName(), user.getEmail());
    }
}
```

Business rules — like "email must be unique" — go here, not in the controller.

---

## Global Exception Handling

Instead of try/catch in every controller, use `@ControllerAdvice` to handle exceptions centrally:

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public Map<String, String> handleNotFound(ResourceNotFoundException e) {
        return Map.of("error", e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public Map<String, String> handleValidation(MethodArgumentNotValidException e) {
        Map<String, String> errors = new HashMap<>();
        e.getBindingResult().getFieldErrors().forEach(fe ->
            errors.put(fe.getField(), fe.getDefaultMessage())
        );
        return errors;
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public Map<String, String> handleGeneric(Exception e) {
        return Map.of("error", "An unexpected error occurred");
    }
}
```

---

## Data Transfer Objects (DTOs)

Don't expose your database entities directly from the API. Use DTOs to control what the client sees.

```java
// Entity (lesson 7) — has database annotations, internal fields
@Entity
public class User {
    @Id private Long id;
    private String name;
    private String email;
    private String passwordHash; // should NEVER appear in API response
}

// DTO — what the client receives
public record UserDto(Long id, String name, String email) {}

// Request — what the client sends
public record CreateUserRequest(
    @NotBlank String name,
    @Email String email,
    @NotBlank String password
) {}
```

The mapping from entity to DTO happens in the service layer. This way, the API contract doesn't change when you refactor the database model.

---

## Common HTTP Status Codes

| Status | When to Return |
|--------|---------------|
| 200 OK | Successful GET, PUT, PATCH |
| 201 Created | Successful POST that creates a resource |
| 204 No Content | Successful DELETE |
| 400 Bad Request | Invalid input, validation failure |
| 401 Unauthorized | Not authenticated |
| 403 Forbidden | Authenticated but not authorized |
| 404 Not Found | Resource doesn't exist |
| 409 Conflict | Resource already exists |
| 500 Internal Server Error | Unexpected server error |

---

## Common Pitfalls

**Putting business logic in the controller**
```java
@PostMapping
public UserDto create(@RequestBody CreateUserRequest req) {
    // Bug: business logic in controller
    if (userRepository.existsByEmail(req.email())) { ... }
    User user = new User(...);
    return userRepository.save(user);
}
```
Controllers should be thin. Logic goes in the service.

**Exposing entities directly**
Returning a JPA entity from a controller can trigger lazy-loading, expose sensitive fields, and leak database structure. Always map to a DTO.

**Not returning the right status code**
Returning 200 for a creation or 200 for a deletion makes the API ambiguous. Use `@ResponseStatus` or `ResponseEntity` to be precise.

---

## Quick Reference

```
Annotations
  @RestController              JSON response, combines @Controller + @ResponseBody
  @RequestMapping("/base")     base path for the class
  @GetMapping("/{id}")         HTTP GET
  @PostMapping                 HTTP POST
  @PutMapping("/{id}")         HTTP PUT
  @DeleteMapping("/{id}")      HTTP DELETE
  @PathVariable Long id        from URL path
  @RequestParam int page       from query string ?page=0
  @RequestBody Foo req         from JSON body
  @Valid                       trigger validation on @RequestBody
  @ResponseStatus(HttpStatus.CREATED)  set status code

ResponseEntity
  ResponseEntity.ok(body)          200
  ResponseEntity.created(uri)      201 + Location header
  ResponseEntity.noContent()       204
  ResponseEntity.notFound()        404
  ResponseEntity.badRequest()      400

Global errors
  @RestControllerAdvice            class handles exceptions globally
  @ExceptionHandler(Foo.class)     method catches specific exception

Validation constraints
  @NotNull  @NotBlank  @Email  @Min(n)  @Max(n)  @Size(min,max)
```
