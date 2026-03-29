import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Collections;
import java.util.Set;

public class Gradebook {

    // Map<String, List<Integer>> = each student name maps to a list of their scores
    private Map<String, List<Integer>> scores = new HashMap<>();

    public void addScore(String name, int score) {
        // computeIfAbsent creates a new list for the student if they don't exist yet,
        // then adds the score — avoids a separate if-check
        scores.computeIfAbsent(name, k -> new ArrayList<>()).add(score);
    }

    public double getAverage(String name) {
        List<Integer> studentScores = scores.get(name);
        if (studentScores == null) return 0.0;

        int total = 0;
        for (int score : studentScores) {
            total += score;
        }

        // cast to double first — otherwise Java does integer division and drops the decimal
        return (double) total / studentScores.size();
    }

    public List<String> getTopStudents(double minAverage) {
        List<String> result = new ArrayList<>();

        for (String name : scores.keySet()) {
            if (getAverage(name) >= minAverage) {
                result.add(name);
            }
        }

        Collections.sort(result);
        return result;
    }

    public Set<String> getAllNames() {
        return scores.keySet();
    }

    // <T extends Comparable<T>> means T can be any type that knows how to compare itself
    // (Integer, String, Double, etc.) — makes this work for any list, not just integers
    public static <T extends Comparable<T>> T findMax(List<T> list) {
        if (list.isEmpty()) throw new IllegalArgumentException("List is empty");

        T max = list.get(0);
        for (T item : list) {
            if (item.compareTo(max) > 0) {
                max = item;
            }
        }
        return max;
    }
}
