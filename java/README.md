# Java Reference Course

A self-paced reference for modern Java and Spring Boot. README-only — concept overview, syntax reference, common pitfalls, and a quick reference card per lesson.

---

## Requirements

- **Java 17+** (Spring Boot 3.x requires it; records/sealed classes require 16+)
- **Maven or Gradle** (lesson 8)
- **Spring Boot 3.x** (lessons 5–7)

---

## Lessons

| # | Topic | What You'll Learn |
|---|-------|------------------|
| 01 | [OOP Fundamentals](01_oop_fundamentals/README.md) | Classes, constructors, access modifiers, encapsulation |
| 02 | [Collections & Generics](02_collections_generics/README.md) | ArrayList, HashMap, HashSet, `<T>`, wildcards |
| 03 | [Java 8 — Lambdas, Streams, Optional](03_java8_lambdas_streams_optional/README.md) | Functional interfaces, Stream API, null safety |
| 04 | [Exceptions, Enums, Records](04_exceptions_enums_records/README.md) | Checked/unchecked exceptions, enums with behavior, records |
| 05 | [Spring Boot Basics](05_spring_boot_basics/README.md) | Auto-config, dependency injection, `@Component`, `@Bean` |
| 06 | [REST Controllers & Services](06_rest_controllers_services/README.md) | `@RestController`, request mapping, service layer |
| 07 | [Spring Data JPA & Hibernate](07_spring_data_jpa_hibernate/README.md) | `@Entity`, `JpaRepository`, relationships, JPQL |
| 08 | [Maven & Gradle](08_maven_gradle/README.md) | `pom.xml`, build lifecycle, Gradle basics |
| 09 | [JUnit Testing](09_junit_testing/README.md) | `@Test`, assertions, Mockito, `@SpringBootTest` |

---

## Recommended Order

Lessons 1–4 are standalone Java — read in any order. Lessons 5–7 are Spring and build on each other sequentially. Lessons 8–9 apply everywhere.

---

## How to Run a Spring Boot App

```bash
# Maven
./mvnw spring-boot:run

# Gradle
./gradlew bootRun
```
