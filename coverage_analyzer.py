import random
import math
import sys
from typing import List, Set, Dict, Union, Tuple
import os
import traceback
import time

class LineTracer:
    def __init__(self):
        self.covered_lines = set()
        
    def trace_lines(self, frame, event, arg):
        if event == 'line':
            self.covered_lines.add(frame.f_lineno)
        return self.trace_lines

class CoverageAnalyzer:
    def __init__(self, source_code: str, problem_type: str):
        self.source_code = source_code
        self.problem_type = problem_type
        
        # Get coverable lines excluding non-coverable elements
        self.lines = []
        self.control_structures = {}  # Maps control structure lines to body lines
        lines = source_code.splitlines()
        
        current_indent = 0
        control_start = None
        body_lines = []
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Skip empty lines, comments, and non-coverable lines
            if (not stripped or 
                stripped.startswith('#') or 
                stripped.startswith(('def ', 'class ', 'import ', 'from ')) or
                (stripped.startswith('return ') and not body_lines)):
                continue
                
            # Track indentation
            indent = len(line) - len(line.lstrip())
            
            # Check if this is a control structure
            if stripped.startswith(('if ', 'for ', 'while ', 'elif ', 'else:')):
                if current_indent < indent:
                    control_start = i
                    body_lines = []
                current_indent = indent
            
            # Add to coverable lines if not a control structure definition
            if not stripped.startswith(('if ', 'for ', 'while ', 'elif ', 'else:')):
                self.lines.append(i)
                
            # Track control structure body lines
            if control_start and indent > current_indent:
                body_lines.append(i)
            elif control_start and body_lines:
                self.control_structures[control_start] = body_lines
                control_start = None
                body_lines = []
        
        self.total_lines = len(self.lines)
        print(f"[DEBUG] Initialized analyzer for {problem_type}")
        print(f"[DEBUG] Total coverable lines: {self.total_lines}")
        print(f"[DEBUG] Coverable line numbers: {self.lines}")
        if self.control_structures:
            print(f"[DEBUG] Control structures: {self.control_structures}")

    def _analyze_source_code(self):
        """Analyze source code to determine coverable lines and control structure relationships"""
        lines = self.source_code.splitlines()
        current_indent = 0
        control_start = None
        body_lines = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
                
            # Skip function definitions, imports, class definitions
            if stripped.startswith(('def ', 'class ', 'import ', 'from ')):
                continue
            
            # Skip standalone return statements (not in control structures)
            if stripped.startswith('return ') and not body_lines:
                continue
            
            # Track indentation
            indent = len(line) - len(line.lstrip())
            
            # Check if this is a control structure start
            if stripped.startswith(('if ', 'for ', 'while ', 'elif ', 'else:')):
                if current_indent < indent:
                    control_start = i
                    body_lines = []
                current_indent = indent
            
            # Add to coverable lines if not a control structure line
            if not stripped.startswith(('if ', 'for ', 'while ', 'elif ', 'else:')):
                self.coverable_lines.append(i)
                
            # Track body lines of control structures
            if control_start and indent > current_indent:
                body_lines.append(i)
            elif control_start and body_lines:
                self.control_structures[control_start] = body_lines
                control_start = None
                body_lines = []

    def evaluate_coverage(self, test_cases: List[Union[str, int]]) : # -> Tuple[Set[int], float]
        """Evaluate coverage using line tracing"""
        print(f"\n[DEBUG] Starting coverage evaluation with {len(test_cases)} test cases")
        covered_lines = set()
        
        try:
            compiled_code = compile(self.source_code, '<string>', 'exec')
            print("[DEBUG] Successfully compiled source code")
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n[DEBUG] Running test case {i}/{len(test_cases)}")
                print(f"[DEBUG] Test input: {test_case}")
                
                try:
                    # Create fresh namespace for each test case
                    namespace = {}
                    exec(compiled_code, namespace)
                    calculate_func = namespace['calculate']
                    
                    # Set up line tracer
                    tracer = LineTracer()
                    sys.settrace(tracer.trace_lines)
                    
                    try:
                        # Execute test case
                        if self.problem_type == "NQUEENS":
                            result = calculate_func(int(test_case) if isinstance(test_case, str) else test_case)
                        else:
                            result = calculate_func(str(test_case).strip())
                        print(f"[DEBUG] Test case result: {result}")
                    finally:
                        sys.settrace(None)
                    
                    # Get covered lines for this test case
                    test_covered = tracer.covered_lines
                    # Only consider lines that are in our filtered set
                    test_covered = test_covered.intersection(set(self.lines))
                    
                    print(f"[DEBUG] Raw covered lines: {sorted(tracer.covered_lines)}")
                    print(f"[DEBUG] Filtered covered lines: {sorted(test_covered)}")
                    
                    # Update control structure coverage
                    for control_line in self.control_structures:
                        if control_line not in test_covered:
                            # If control structure not covered, its body shouldn't be counted
                            body_lines = self.control_structures[control_line]
                            test_covered = test_covered - set(body_lines)
                            print(f"[DEBUG] Removed body lines for control structure at line {control_line}: {body_lines}")
                    
                    covered_lines.update(test_covered)
                    print(f"[DEBUG] Cumulative covered lines: {sorted(covered_lines)}")
                    
                except Exception as e:
                    print(f"[DEBUG] Test case failed: {str(e)}")
                    traceback.print_exc()
                    continue
            
            # Calculate final coverage
            uncovered_lines = set(self.lines) - covered_lines
            coverage_percentage = (len(covered_lines) / len(self.lines) * 100) if self.lines else 0.0
            
            print(f"\n[DEBUG] Final Coverage Results:")
            print(f"Total lines to cover: {len(self.lines)}")
            print(f"Lines actually covered: {len(covered_lines)}")
            print(f"Lines uncovered: {len(uncovered_lines)}")
            print(f"Coverage percentage: {coverage_percentage:.2f}%")
            
            return uncovered_lines, coverage_percentage
                
        except Exception as e:
            print(f"[ERROR] Coverage analysis failed: {str(e)}")
            traceback.print_exc()
            return set(self.lines), 0.0

    def hill_climbing(self, iterations: int = 50) : # -> Tuple[Set[int], float, List[str]]
        """Use hill climbing to find test cases that maximize coverage"""
        current_test_cases = self.get_initial_test_cases()
        current_uncovered, current_score = self.evaluate_coverage(current_test_cases)
        
        best_test_cases = current_test_cases.copy()
        best_uncovered = current_uncovered
        best_score = current_score
        
        print(f"\n[DEBUG] Starting hill climbing with {iterations} iterations")
        print(f"[DEBUG] Initial coverage: {current_score:.2f}%")
        
        for i in range(iterations):
            print(f"\n[DEBUG] Hill climbing iteration {i+1}/{iterations}")
            
            neighbor_test_cases = current_test_cases.copy()
            idx = random.randint(0, len(neighbor_test_cases)-1)
            neighbor_test_cases[idx] = self.mutate_test_case(neighbor_test_cases[idx])
            
            neighbor_uncovered, neighbor_score = self.evaluate_coverage(neighbor_test_cases)
            
            if neighbor_score > current_score:
                print(f"[DEBUG] Found better solution: {neighbor_score:.2f}% > {current_score:.2f}%")
                current_test_cases = neighbor_test_cases
                current_score = neighbor_score
                current_uncovered = neighbor_uncovered
                
                if current_score > best_score:
                    print(f"[DEBUG] New best score: {current_score:.2f}%")
                    best_score = current_score
                    best_test_cases = current_test_cases.copy()
                    best_uncovered = current_uncovered
                    
            if best_score >= 100:
                print("[DEBUG] Achieved perfect coverage, stopping early")
                break
                
        print(f"\n[DEBUG] Hill climbing complete")
        print(f"Final best score: {best_score:.2f}%")
        print(f"Uncovered lines: {sorted(best_uncovered)}")
        
        return best_uncovered, best_score, best_test_cases

    def simulated_annealing(self, initial_temperature: float = 1.0, 
                          cooling_rate: float = 0.95, 
                          iterations: int = 100) : # -> Tuple[Set[int], float, List[str]]
        """Use simulated annealing to find optimal test cases"""
        current_test_cases = self.get_initial_test_cases()
        current_uncovered, current_score = self.evaluate_coverage(current_test_cases)
        
        best_test_cases = current_test_cases.copy()
        best_uncovered = current_uncovered
        best_score = current_score
        
        temperature = initial_temperature
        
        print(f"\n[DEBUG] Starting simulated annealing")
        print(f"[DEBUG] Initial temperature: {temperature}")
        print(f"[DEBUG] Initial coverage: {current_score:.2f}%")
        
        for i in range(iterations):
            print(f"\n[DEBUG] SA iteration {i+1}/{iterations}")
            print(f"[DEBUG] Current temperature: {temperature:.4f}")
            
            # Create neighbor with temperature-based mutations
            neighbor_test_cases = current_test_cases.copy()
            mutations = max(1, int(temperature * 3))
            
            for _ in range(mutations):
                idx = random.randint(0, len(neighbor_test_cases)-1)
                neighbor_test_cases[idx] = self.mutate_test_case(neighbor_test_cases[idx], temperature)
            
            neighbor_uncovered, neighbor_score = self.evaluate_coverage(neighbor_test_cases)
            score_diff = neighbor_score - current_score
            
            # Accept or reject based on score and temperature
            if score_diff > 0 or random.random() < math.exp(score_diff / temperature):
                print(f"[DEBUG] Accepted new solution with score {neighbor_score:.2f}%")
                current_test_cases = neighbor_test_cases
                current_score = neighbor_score
                current_uncovered = neighbor_uncovered
                
                if current_score > best_score:
                    print(f"[DEBUG] New best score: {current_score:.2f}%")
                    best_score = current_score
                    best_test_cases = current_test_cases.copy()
                    best_uncovered = current_uncovered
            
            temperature *= cooling_rate
            
            if best_score >= 100:
                print("[DEBUG] Achieved perfect coverage, stopping early")
                break
        
        print(f"\n[DEBUG] Simulated annealing complete")
        print(f"Final best score: {best_score:.2f}%")
        print(f"Uncovered lines: {sorted(best_uncovered)}")
        
        return best_uncovered, best_score, best_test_cases

    def get_initial_test_cases(self): # -> List[str]:
        """Get initial test cases based on problem type"""
        if self.problem_type == "SCC":
            return [
                "1 0\n",
                "2 2\n1 2\n2 1",
                "3 3\n1 2\n2 3\n3 1",
                "4 4\n1 2\n2 3\n3 4\n4 1"
            ]
        elif self.problem_type == "BRIDGE":
            return [
                "4 4\n1 1 0 0\n1 1 0 0\n0 0 1 1\n0 0 1 1",
                "4 4\n1 0 0 1\n0 0 0 0\n0 0 0 0\n1 0 0 1",
                "5 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1\n0 0 0 1 1"
            ]
        elif self.problem_type == "MST":
            return [
                # Basic test case
                "2 1\n1 2 1\n",
                # Triangle with different weights
                "3 3\n1 2 1\n2 3 2\n1 3 3\n",
                # Negative weights
                "3 3\n1 2 -1\n2 3 -2\n1 3 1\n",
                # Larger test case
                "4 5\n1 2 10\n2 3 20\n3 4 30\n4 1 40\n1 3 50\n",
                # Single vertex
                "1 0\n"
            ]
        elif self.problem_type == "NQUEENS":
            # Return integers directly for N-Queens
            return [1, 2, 3, 4, 5, 6, 7, 8]  # Testing different board sizes
        return []

    def mutate_test_case(self, test_case: str, temperature: float = None) : # -> str
        """Mutate test case with temperature-based probability"""
        mutation_strength = temperature if temperature is not None else 0.5

        if self.problem_type == "SCC":
            # SCC mutation (your existing code)
            lines = test_case.strip().split("\n")
            V, E = map(int, lines[0].split())
            edges = [tuple(map(int, line.split())) for line in lines[1:]]
            
            mutations = [
                (lambda: edges.append((random.randint(1, V), random.randint(1, V))), 0.3),
                (lambda: edges.pop(random.randint(0, len(edges)-1)) if edges else None, 0.2),
                (lambda: edges.__setitem__(random.randint(0, len(edges)-1), 
                                         (random.randint(1, V), random.randint(1, V))), 0.3),
                (lambda: V + random.choice([-1, 1]) if V > 1 else V + 1, 0.1)
            ]
            
            for mutation, prob in mutations:
                if random.random() < prob * mutation_strength:
                    try:
                        mutation()
                    except Exception:
                        continue
            
            return f"{V} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges)

        elif self.problem_type == "BRIDGE":
            lines = test_case.strip().split("\n")
            N, M = map(int, lines[0].split())
            grid = [list(map(int, line.split())) for line in lines[1:]]
            
            mutations = [
                # Flip random cell
                (lambda: self._flip_cell(grid), 0.4),
                # Add new island
                (lambda: self._add_island(grid), 0.3),
                # Remove island
                (lambda: self._remove_island(grid), 0.3)
            ]
            
            for mutation, prob in mutations:
                if random.random() < prob * mutation_strength:
                    try:
                        mutation()
                    except Exception:
                        continue
            
            return f"{N} {M}\n" + "\n".join(" ".join(map(str, row)) for row in grid)

        elif self.problem_type == "MST":
            lines = test_case.strip().split("\n")
            V, E = map(int, lines[0].split())
            edges = [tuple(map(int, line.split())) for line in lines[1:]]
            
            mutations = [
                # Add edge
                (lambda: edges.append((random.randint(1, V), random.randint(1, V), 
                                    random.randint(-10, 10))), 0.3),
                # Remove edge
                (lambda: edges.pop(random.randint(0, len(edges)-1)) if edges else None, 0.2),
                # Modify weight
                (lambda: self._modify_weight(edges), 0.3),
                # Add vertex
                (lambda: V + 1 if random.random() < 0.1 else V, 0.2)
            ]
            
            for mutation, prob in mutations:
                if random.random() < prob * mutation_strength:
                    try:
                        mutation()
                    except Exception:
                        continue
            
            return f"{V} {len(edges)}\n" + "\n".join(f"{a} {b} {w}" for a, b, w in edges)

        elif self.problem_type == "NQUEENS":
            # Convert to int if it's a string
            n = int(test_case) if isinstance(test_case, str) else test_case
            # Randomly increase or decrease board size within bounds
            if random.random() < mutation_strength:
                n = max(1, min(9, n + random.choice([-1, 1])))
            return n  # Return integer directly

        return test_case

    # Helper functions for mutations
    def _flip_cell(self, grid):
        """Flip a random cell in the grid"""
        i = random.randint(0, len(grid)-1)
        j = random.randint(0, len(grid[0])-1)
        grid[i][j] = 1 - grid[i][j]

    def _add_island(self, grid):
        """Add a small island at random position"""
        i = random.randint(0, len(grid)-2)
        j = random.randint(0, len(grid[0])-2)
        grid[i][j] = grid[i+1][j] = grid[i][j+1] = grid[i+1][j+1] = 1

    def _remove_island(self, grid):
        """Remove an island at random position"""
        i = random.randint(0, len(grid)-2)
        j = random.randint(0, len(grid[0])-2)
        grid[i][j] = grid[i+1][j] = grid[i][j+1] = grid[i+1][j+1] = 0

    def _modify_weight(self, edges):
        """Modify weight of a random edge"""
        if edges:
            idx = random.randint(0, len(edges)-1)
            a, b, _ = edges[idx]
            edges[idx] = (a, b, random.randint(-10, 10))

def get_line_content(source_code: str, line_number: int) : # -> str
    """Get content of a specific line from source code"""
    lines = source_code.splitlines()
    if 1 <= line_number <= len(lines):
        return lines[line_number - 1].strip()
    return "Line not found"

def generate_coverage_report(problem_dir: str, solution_file: str) : # -> str
    """Generate coverage report with uncovered code lines"""
    try:
        # Read files
        with open(os.path.join(problem_dir, 'description.txt'), 'r') as f:
            description = f.read()
        with open(solution_file, 'r') as f:
            source_code = f.read()
        
        # Determine problem type
        if "Strongly Connected Components" in description:
            problem_type = "SCC"
        elif "Bridge Building" in description:
            problem_type = "BRIDGE"
        elif "Minimum Spanning Tree" in description:
            problem_type = "MST"
        elif "N Queens" in description:
            problem_type = "NQUEENS"
        else:
            problem_type = "UNKNOWN"
        
        # Run simulated annealing
        analyzer = CoverageAnalyzer(source_code, problem_type)
        uncovered_lines, coverage_percentage, test_cases = analyzer.simulated_annealing(
            initial_temperature=1.0,
            cooling_rate=0.95,
            iterations=50
        )
        
        # Generate report
        report = f"Coverage Report\n{'='*50}\n"
        report += f"Coverage Percentage: {coverage_percentage:.2f}%\n\n"
        
        # Add uncovered lines section
        report += "Uncovered Code Lines:\n"
        report += "-" * 50 + "\n"
        for line_num in sorted(uncovered_lines):
            line_content = get_line_content(source_code, line_num)
            report += f"Line {line_num}: {line_content}\n"
        report += "-" * 50 + "\n\n"
        
        # Add the standard coverage format
        report += "Not coverd = {\n"
        for line in sorted(uncovered_lines):
            line_content = get_line_content(source_code, line)
            report += f"    (calculate(s),{line}),  # {line_content}\n"
        report += "}"
        
        return report
        
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        traceback.print_exc()  # Print full error trace for debugging
        return "Error generating coverage report"

def process_all_solutions(base_dir: str = 'data'):
    """Process all solutions and generate coverage reports"""
    for problem_dir in os.listdir(base_dir):
        problem_path = os.path.join(base_dir, problem_dir)
        if not os.path.isdir(problem_path):
            continue
            
        solution_dir = os.path.join(problem_path, 'solution')
        coverage_dir = os.path.join(problem_path, 'coverage')
        os.makedirs(coverage_dir, exist_ok=True)
        
        solution_files = [f for f in os.listdir(solution_dir) 
                         if f.startswith(f'{problem_dir}_solution_') and f.endswith('.py')]
        
        for solution_file in sorted(solution_files):
            try:
                solution_path = os.path.join(solution_dir, solution_file)
                print(f"\n[DEBUG] Processing {solution_file}")
                
                coverage_report = generate_coverage_report(problem_path, solution_path)
                
                coverage_file = os.path.join(coverage_dir, f"{os.path.splitext(solution_file)[0]}_cv.txt")
                with open(coverage_file, 'w') as f:
                    f.write(coverage_report)
                
                print(f"Generated coverage report for {solution_file}")
                
            except Exception as e:
                print(f"Error processing {solution_file}: {str(e)}")

if __name__ == "__main__":
    print("processing to create coverage report...")
    start_time = time.time()
    process_all_solutions()
    end_time = time.time()
    print("coverage report generated successfully...!!!")
    print("time taken to run the code is ", end_time-start_time)