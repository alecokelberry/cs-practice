public class Main {
    public static void main(String[] args) {
        Student student1 = new Student ("Alice", 1001, 3.5);
        Student student2 = new Student ("Bob", 1002, 2.8);
        Student student3 = new Student ("Carol", 1003, 3.9);

        System.out.println(student1);
        System.out.println(student2);
        System.out.println(student3);

        System.out.println("Total students: " + Student.getStudentCount());

        try {
            Student student4 = new Student ("Dave", 1004, 5.0);
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
