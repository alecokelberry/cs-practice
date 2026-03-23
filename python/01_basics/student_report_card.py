try:
    name: str = input("Enter name: ")
    age: int = int(input("Enter age: "))
    math_score: float = float(input("Enter Math score (0-100): "))
    english_score: float = float(input("Enter English score (0-100): "))
    science_score: float = float(input("Enter Science score (0-100): "))

except ValueError:
    print("Pleae enter valid numbers for age and scores.")
    exit(1)

average: float = (math_score + english_score + science_score) / 3

def letter_grade(score: float) -> str:
    match score:
        case n if n >= 90: return "A"
        case n if n >= 80: return "B"
        case n if n >= 70: return "C"
        case n if n >= 60: return "D"
        case _:            return "F"    

subjects = [("Math", math_score), ("English", english_score), ("Science", science_score)]

print("-" * 25)
print(f"Name: {name}")
print(f"Age: {age}")

print("-" * 25)
print(f"{'Subject':<10} {'Score':>6} Grade")
print("-" * 25)

for subject, score in subjects:
    print(f"{subject:<10} {score:>6.2f} {letter_grade(score)}")
print("-" * 25)

print(f"{'Average':<10} {average:>6.2f} {letter_grade(average)}")
print("-" * 25)