# 09 — JUnit Testing

Testing in Java has two layers: **unit tests** (one class in isolation, dependencies replaced with mocks) and **integration tests** (the Spring context wired up, hitting a real or in-memory database). JUnit 5 is the test framework; Mockito handles mocking.

`spring-boot-starter-test` includes both — no extra dependencies needed.

---

## JUnit 5 Basics

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {

    private Calculator calc;

    @BeforeEach
    void setUp() {
        calc = new Calculator(); // fresh instance before each test
    }

    @AfterEach
    void tearDown() {
        // cleanup after each test (rarely needed)
    }

    @BeforeAll
    static void beforeAll() {
        // runs once before all tests in this class (expensive setup)
    }

    @Test
    void add_twoPositiveNumbers_returnsSum() {
        int result = calc.add(2, 3);
        assertEquals(5, result);
    }

    @Test
    void divide_byZero_throwsException() {
        assertThrows(ArithmeticException.class, () -> calc.divide(10, 0));
    }

    @Test
    @Disabled("Not implemented yet")
    void futureFeature() { }
}
```

### Naming Convention

Use **`methodName_scenario_expectedBehavior`**:
- `findById_existingUser_returnsUser`
- `create_duplicateEmail_throwsException`
- `delete_nonexistentId_returnsNotFound`

This makes failing tests self-describing — you know what broke and why without reading the test body.

---

## Assertions

```java
// Equality
assertEquals(expected, actual);
assertNotEquals(unexpected, actual);

// Null checks
assertNull(value);
assertNotNull(value);

// Booleans
assertTrue(condition);
assertFalse(condition);

// Exceptions
assertThrows(IllegalArgumentException.class, () -> {
    service.create(null);
});

// Exception with message check
var ex = assertThrows(IllegalArgumentException.class, () -> service.create(null));
assertTrue(ex.getMessage().contains("must not be null"));

// Collections
assertIterableEquals(List.of("a", "b"), result);

// Multiple assertions — all run even if one fails
assertAll(
    () -> assertEquals("Alice", user.getName()),
    () -> assertEquals("alice@example.com", user.getEmail()),
    () -> assertNotNull(user.getId())
);

// Custom message (shown when assertion fails)
assertEquals(5, result, "Expected result to be 5 after adding 2 + 3");
```

---

## AssertJ (Fluent Assertions)

AssertJ is included with `spring-boot-starter-test` and provides more readable assertions:

```java
import static org.assertj.core.api.Assertions.*;

assertThat(result).isEqualTo(5);
assertThat(name).isEqualTo("Alice").startsWith("Ali").hasSize(5);
assertThat(list).hasSize(3).contains("apple").doesNotContain("orange");
assertThat(optional).isPresent().contains("value");
assertThat(map).containsKey("name").containsEntry("name", "Alice");

// Exception assertion
assertThatThrownBy(() -> service.delete(-1))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessageContaining("invalid id");
```

---

## Mockito — Unit Testing with Mocks

A **mock** is a fake object that you control. You tell it what to return when called, then verify it was called correctly. This lets you test a class in complete isolation.

### Setup

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.assertj.core.api.Assertions.*;

@ExtendWith(MockitoExtension.class) // activates Mockito for this test class
class UserServiceTest {

    @Mock
    private UserRepository userRepository; // Mockito creates a mock

    @InjectMocks
    private UserService userService; // Mockito injects mocks into this

    @Test
    void findById_existingUser_returnsDto() {
        // Arrange — tell the mock what to return
        User user = new User("Alice", "alice@example.com");
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));

        // Act — call the real code
        Optional<UserDto> result = userService.findById(1L);

        // Assert — check the result
        assertThat(result).isPresent();
        assertThat(result.get().name()).isEqualTo("Alice");
    }

    @Test
    void create_duplicateEmail_throwsException() {
        when(userRepository.existsByEmail("alice@example.com")).thenReturn(true);

        assertThatThrownBy(() -> userService.create(new CreateUserRequest("Alice", "alice@example.com")))
            .isInstanceOf(DuplicateEmailException.class);

        // Verify save was never called
        verify(userRepository, never()).save(any());
    }

    @Test
    void findAll_multipleUsers_returnsMappedDtos() {
        List<User> users = List.of(
            new User("Alice", "alice@example.com"),
            new User("Bob", "bob@example.com")
        );
        when(userRepository.findAll()).thenReturn(users);

        List<UserDto> result = userService.findAll();

        assertThat(result).hasSize(2);
        verify(userRepository).findAll(); // verify it was called exactly once
    }
}
```

### Mockito Stubbing

```java
// Return a value
when(repo.findById(1L)).thenReturn(Optional.of(user));

// Return different values on successive calls
when(repo.findAll())
    .thenReturn(List.of(user1))
    .thenReturn(List.of(user1, user2)); // second call

// Throw an exception
when(repo.findById(99L)).thenThrow(new ResourceNotFoundException("99"));

// Return nothing (void method — default behavior, but explicit)
doNothing().when(repo).deleteById(1L);

// Throw from void method
doThrow(new RuntimeException()).when(repo).deleteById(-1L);

// Argument matchers
when(repo.findById(anyLong())).thenReturn(Optional.empty());
when(repo.findByEmail(eq("alice@example.com"))).thenReturn(Optional.of(user));
when(repo.save(any(User.class))).thenReturn(savedUser);
```

### Mockito Verification

```java
verify(repo).save(any(User.class));         // called exactly once
verify(repo, times(2)).findAll();           // called exactly twice
verify(repo, never()).deleteById(anyLong()); // never called
verify(repo, atLeastOnce()).findById(1L);   // called at least once

// Capture the argument passed to a method
ArgumentCaptor<User> captor = ArgumentCaptor.forClass(User.class);
verify(repo).save(captor.capture());
User saved = captor.getValue();
assertThat(saved.getName()).isEqualTo("Alice");
```

---

## Parameterized Tests

Run the same test with multiple inputs:

```java
@ParameterizedTest
@ValueSource(strings = {"", " ", "\t"})
void create_blankName_throwsException(String blankName) {
    assertThatThrownBy(() -> service.create(new CreateUserRequest(blankName, "a@b.com")))
        .isInstanceOf(IllegalArgumentException.class);
}

@ParameterizedTest
@CsvSource({
    "2, 3, 5",
    "10, -5, 5",
    "0, 0, 0"
})
void add_variousInputs_returnsSum(int a, int b, int expected) {
    assertEquals(expected, calc.add(a, b));
}

@ParameterizedTest
@MethodSource("provideUsers")
void create_validUser_succeeds(String name, String email) {
    // ...
}

static Stream<Arguments> provideUsers() {
    return Stream.of(
        Arguments.of("Alice", "alice@example.com"),
        Arguments.of("Bob", "bob@example.com")
    );
}
```

---

## Spring Integration Tests

Integration tests start a real Spring context. They're slower but verify that the wiring, configuration, and database access all work together.

### `@SpringBootTest`

```java
@SpringBootTest          // loads the full application context
@AutoConfigureMockMvc    // configures MockMvc automatically
class UserControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }

    @Test
    void getUser_existingId_returns200() throws Exception {
        User saved = userRepository.save(new User("Alice", "alice@example.com"));

        mockMvc.perform(get("/api/users/" + saved.getId()))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("Alice"))
            .andExpect(jsonPath("$.email").value("alice@example.com"));
    }

    @Test
    void createUser_validRequest_returns201() throws Exception {
        String json = """
            {"name": "Bob", "email": "bob@example.com"}
            """;

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(json))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.name").value("Bob"));
    }
}
```

### `@DataJpaTest`

Loads only the JPA layer — no web layer. Uses an in-memory H2 database by default. Fast.

```java
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private UserRepository userRepository;

    @Test
    void findByEmail_existingUser_returnsUser() {
        userRepository.save(new User("Alice", "alice@example.com"));

        Optional<User> found = userRepository.findByEmail("alice@example.com");

        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("Alice");
    }

    @Test
    void existsByEmail_duplicateEmail_returnsTrue() {
        userRepository.save(new User("Alice", "alice@example.com"));
        assertThat(userRepository.existsByEmail("alice@example.com")).isTrue();
    }
}
```

---

## Test Layers Cheat Sheet

| Test Type | Annotation | Spring Context | Speed | What to Test |
|-----------|------------|---------------|-------|-------------|
| Unit | `@ExtendWith(MockitoExtension.class)` | None | Fast | Service logic in isolation |
| Repository | `@DataJpaTest` | JPA only | Medium | Queries, custom methods |
| Controller | `@WebMvcTest` | Web only | Medium | HTTP mapping, validation |
| Integration | `@SpringBootTest` | Full | Slow | End-to-end wiring |

---

## Common Pitfalls

**Testing implementation, not behavior**
```java
// Bad — testing that a specific method was called (brittle)
verify(userRepository).findById(1L);

// Better — test what the caller cares about (the result)
assertThat(result).isPresent();
assertThat(result.get().name()).isEqualTo("Alice");
```

**Not resetting state between tests**
Tests should be independent. If one test creates a user in the database and the next test assumes it's empty, tests fail randomly depending on run order. Use `@BeforeEach` to clean up or `@Transactional` to roll back after each test.

**Testing Spring's behavior**
Don't test that `@Valid` rejects null — Spring does that, not you. Test your own validation logic and business rules.

---

## Quick Reference

```
JUnit 5
  @Test                        test method
  @BeforeEach / @AfterEach     run before/after each test
  @BeforeAll / @AfterAll       run once before/after all tests (static)
  @Disabled("reason")          skip test
  @ParameterizedTest           multiple inputs
  @ValueSource / @CsvSource / @MethodSource  parameterized inputs

Assertions (JUnit)
  assertEquals(expected, actual)
  assertThrows(Foo.class, () -> code())
  assertAll(() -> ..., () -> ...)

Assertions (AssertJ)
  assertThat(x).isEqualTo(y)
  assertThat(list).hasSize(n).contains(e)
  assertThatThrownBy(() -> x).isInstanceOf(Foo.class).hasMessageContaining("msg")

Mockito
  @ExtendWith(MockitoExtension.class) on class
  @Mock Repo repo               create mock
  @InjectMocks Service svc      inject mocks into this
  when(repo.method(arg)).thenReturn(val)
  when(repo.method(any())).thenThrow(new Foo())
  verify(repo).method(arg)
  verify(repo, never()).method(any())
  ArgumentCaptor<T> cap = ArgumentCaptor.forClass(T.class)
  verify(repo).save(cap.capture()); cap.getValue()

Spring test annotations
  @SpringBootTest               full context
  @DataJpaTest                  JPA layer only, H2
  @AutoConfigureMockMvc         configures MockMvc
  @Autowired MockMvc mockMvc    make HTTP requests in tests
```
