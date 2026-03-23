# 08 — Maven & Gradle

Maven and Gradle are Java build tools. They manage dependencies (like `npm` for Node), compile code, run tests, and package the app into a runnable JAR. Maven uses XML config (`pom.xml`); Gradle uses a Groovy or Kotlin DSL (`build.gradle`).

Spring Boot projects can use either. Maven is more common in enterprise environments; Gradle is faster and more flexible.

---

## Maven

### `pom.xml` Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <!-- Project coordinates — unique identifier for this artifact -->
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <packaging>jar</packaging>

    <!-- Spring Boot parent — inherits default config for all Spring Boot projects -->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
    </parent>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <!-- Spring Web MVC -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <!-- No version needed — inherited from parent -->
        </dependency>

        <!-- Spring Data JPA -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- Test scope — only included in test compilation/runtime -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Creates an executable "fat JAR" with all dependencies bundled -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

### Dependency Scopes

| Scope | Classpath | Packaged | Use |
|-------|-----------|----------|-----|
| `compile` (default) | Compile + Runtime | Yes | Main dependencies |
| `test` | Test only | No | JUnit, Mockito |
| `runtime` | Runtime only | Yes | JDBC drivers |
| `provided` | Compile only | No | Servlet API (container provides it) |

### Maven Build Lifecycle

Maven has a fixed sequence of phases. Running a phase runs all phases before it too.

```
validate → compile → test → package → verify → install → deploy
```

| Phase | What It Does |
|-------|-------------|
| `compile` | Compile `src/main/java` |
| `test` | Compile and run `src/test/java` |
| `package` | Create a JAR in `target/` |
| `install` | Copy JAR to `~/.m2` (local Maven repository) |
| `deploy` | Publish JAR to a remote repository |

```bash
./mvnw compile          # compile only
./mvnw test             # compile + test
./mvnw package          # compile + test + JAR
./mvnw package -DskipTests  # skip tests (not recommended in CI)
./mvnw spring-boot:run  # run the app
./mvnw dependency:tree  # show all dependencies and transitive deps
```

`./mvnw` is the Maven Wrapper — a script checked into the repo that downloads the correct Maven version. No local Maven install required.

### The Local Repository (`~/.m2`)

When Maven downloads a dependency, it caches it in `~/.m2/repository`. The next build reuses the cache instead of downloading again. This is shared across all your local Maven projects.

---

## Gradle

### `build.gradle` (Groovy DSL)

```groovy
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.2.0'
    id 'io.spring.dependency-management' version '1.1.4'
}

group = 'com.example'
version = '0.0.1-SNAPSHOT'

java {
    sourceCompatibility = '17'
}

repositories {
    mavenCentral() // where to download dependencies from
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    runtimeOnly 'org.postgresql:postgresql'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}

tasks.named('test') {
    useJUnitPlatform()
}
```

### `build.gradle.kts` (Kotlin DSL — modern preference)

```kotlin
plugins {
    java
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
}

group = "com.example"
version = "0.0.1-SNAPSHOT"

java {
    sourceCompatibility = JavaVersion.VERSION_17
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    runtimeOnly("org.postgresql:postgresql")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

### Gradle Dependency Configurations

| Configuration | Equivalent Maven Scope | Use |
|---------------|----------------------|-----|
| `implementation` | `compile` | Main dependencies |
| `testImplementation` | `test` | Test-only |
| `runtimeOnly` | `runtime` | Drivers, logging implementations |
| `compileOnly` | `provided` | Annotations processed at compile time |
| `annotationProcessor` | — | Lombok, MapStruct |

### Gradle Commands

```bash
./gradlew build             # compile + test + JAR
./gradlew test              # run tests
./gradlew bootRun           # run the Spring Boot app
./gradlew dependencies      # show dependency tree
./gradlew tasks             # list all available tasks
./gradlew clean build       # clean output, then full build
```

`./gradlew` is the Gradle Wrapper — same concept as Maven Wrapper.

---

## Maven vs Gradle — Side by Side

| | Maven | Gradle |
|---|-------|--------|
| Config format | XML (`pom.xml`) | Groovy or Kotlin DSL |
| Build model | Fixed lifecycle | Task graph (more flexible) |
| Speed | Slower | Faster (incremental, caching) |
| Learning curve | Lower | Higher |
| IDE support | Excellent | Excellent |
| Enterprise adoption | Higher | Growing fast |
| Multi-project builds | Supported | Stronger support |

**Choose Maven** if you're joining an existing enterprise project (likely already on Maven) or want convention over configuration.

**Choose Gradle** for new projects that need fast builds, Android, or complex multi-module setups.

---

## Finding Dependencies

Search [mvnrepository.com](https://mvnrepository.com) or [search.maven.org](https://search.maven.org) for any library. Copy the Maven or Gradle snippet and paste it into your build file.

Popular Spring Boot starters:

| Starter | What It Adds |
|---------|-------------|
| `spring-boot-starter-web` | Spring MVC, Tomcat, Jackson |
| `spring-boot-starter-data-jpa` | JPA, Hibernate, Spring Data |
| `spring-boot-starter-security` | Spring Security |
| `spring-boot-starter-validation` | Bean Validation, Hibernate Validator |
| `spring-boot-starter-test` | JUnit 5, Mockito, AssertJ |
| `spring-boot-starter-actuator` | Health endpoints, metrics |

---

## Common Pitfalls

**Version conflicts**
Two dependencies pull in different versions of the same library. Maven uses the "nearest definition wins" rule (closest to root in the dependency tree). Gradle uses the newest version by default. Both can be overridden by declaring the dependency explicitly.

**Not using the wrapper**
Always use `./mvnw` or `./gradlew` — not a locally installed `mvn` or `gradle`. The wrapper ensures everyone on the team (and CI) uses the exact same build tool version.

**`-SNAPSHOT` versions in production**
`SNAPSHOT` means the artifact is unstable and subject to change. Never depend on SNAPSHOTs in production.

---

## Quick Reference

```
Maven
  pom.xml                      config file
  ./mvnw compile               compile
  ./mvnw test                  compile + test
  ./mvnw package               compile + test + JAR in target/
  ./mvnw spring-boot:run       run app
  ./mvnw dependency:tree       show dependency graph
  Dependency scopes: compile (default), test, runtime, provided

Gradle
  build.gradle / build.gradle.kts    config file
  ./gradlew build              compile + test + JAR
  ./gradlew test               run tests
  ./gradlew bootRun            run Spring Boot app
  ./gradlew dependencies       show dependency tree
  ./gradlew tasks              list all tasks
  Configurations: implementation, testImplementation, runtimeOnly, compileOnly

Common Spring Boot starters
  spring-boot-starter-web      REST APIs
  spring-boot-starter-data-jpa JPA + Hibernate
  spring-boot-starter-test     JUnit 5 + Mockito
  spring-boot-starter-validation  @Valid + constraint annotations
```
