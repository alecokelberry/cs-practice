public class Student {
    // Private fields (instance variables)
    private String name;
    private int studentId;
    private double gpa; 
    private static int studentCount = 0;

    // Constructor
    public Student(String name, int studentId, double gpa) {
        this.name = name;
        this.studentId = studentId;
        if (gpa < 0.0 || gpa > 4.0) throw new IllegalArgumentException("GPA must be between 0.0 and 4.0.");
        this.gpa = gpa;
        studentCount++;
    }

    // Getters for all three instance fields
    public String getName() {
        return name;
    }
    public int getStudentId() {
        return studentId;
    }
    public double getGpa() {
        return gpa;
    }

    // Static getStudentCount() method
    public static int getStudentCount() {
        return studentCount;
    }

    // Override toString()
    @Override
    public String toString() {
        return "Student[id=" + studentId + ", name=" + name + ", gpa=" + gpa + "]"; 
    }
}