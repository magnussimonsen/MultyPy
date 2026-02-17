import random
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class MathProblem:
    factor_a: int
    factor_b: int
    answer: int
    options: List[int] = None  # For Simple Mode

class MathGenerator:
    @staticmethod
    def generate_problem(table_range: int, simple_mode: bool = False) -> MathProblem:
        a = random.randint(1, table_range)
        b = random.randint(1, table_range)
        # Ensure we don't just get 1x1 all the time, maybe weight it? 
        # For now, simple random is fine based on specs.
        
        answer = a * b
        problem = MathProblem(factor_a=a, factor_b=b, answer=answer)
        
        if simple_mode:
            options = {answer}
            while len(options) < 3:
                # Generate plausible wrong answers
                offset = random.randint(-5, 5)
                if offset == 0:
                    continue
                wrong_answer = answer + offset
                if wrong_answer > 0:
                    options.add(wrong_answer)
                # Fallback purely random if plausible fails
                if len(options) < 3:
                     options.add(random.randint(1, table_range * table_range))
                     
            problem.options = list(options)
            random.shuffle(problem.options)
            
        return problem
