import java.util.List;

public class Main {
    public static void main(String[] args) {
        Gradebook gb = new Gradebook();

        gb.addScore("Alice", 92);
        gb.addScore("Alice", 88);
        gb.addScore("Alice", 95);

        gb.addScore("Bob", 70);
        gb.addScore("Bob", 74);
        gb.addScore("Bob", 68);

        gb.addScore("Carol", 85);
        gb.addScore("Carol", 90);
        gb.addScore("Carol", 88);

        // getAllNames() returns a Set so print order may vary each run
        for (String name : gb.getAllNames()) {
            System.out.println(name + ": " + gb.getAverage(name));
        }

        System.out.println();
        System.out.println("Top students (avg >= 85): " + gb.getTopStudents(85));

        // List.of() creates an unmodifiable list
        List<Integer> scores = List.of(43, 91, 67, 55, 82);
        System.out.println("Max score: " + Gradebook.findMax(scores));
        System.out.println("All students: " + gb.getAllNames());
    }
}
