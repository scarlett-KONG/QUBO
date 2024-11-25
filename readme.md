# Quantum Annealing and Binary Quadratic Models

This page primarily follows the tutorial series from D-Wave: [YouTube Link](https://youtu.be/teraaPiaG8s?feature=shared)

## What is Quantum Annealing

1. First Paper to start all these: [Equation of State Calculations by Fast Computing Machines](https://people.umass.edu/bvs/The_1953_paper.pdf)

2. Quantum annealing starting paper: [Quantum annealing in the transverse Ising model](https://arxiv.org/abs/cond-mat/9804280)

### Adiabatic Quantum Optimization (AQO)

Referring to Paper [2], we introduce the problem of Adiabatic Quantum Optimization (AQO).

We first provide the trick about how to use AQO to solve NP-complete and NP-hard problems.

Suppose we have a quantum Hamiltonian $H_P$ whose ground state encodes the solution to a problem of interest, and another Hamiltonian $H_0$, whose ground state is "easy" (both to find and to prepare in an experimental setup). Then, if we prepare a quantum system to be in the ground state of $H_0$, and then adiabatically change the Hamiltonian for a time $T$ according to:
$$
H(t) = \left(1 - \frac{t}{T}\right) H_0 + \frac{t}{T} H_P
$$
then if $T$ is large enough, and $H_0$ and $H_P$ do not commute, the quantum system will remain in the ground state for all times, by the adiabatic theorem of quantum mechanics. At time $T$, measuring the quantum state will return a solution to our problem.

Then there comes a debate: whether or not these algorithms would actually be useful, i.e., whether an adiabatic quantum optimizer would run any faster than classical algorithms. This is due to the fact that if the problem has size $N$, one typically finds:
$$
T = O \left[\exp(\alpha N^{\beta})\right]
$$
in order for the system to remain in the ground state, for positive coefficients $\alpha$ and $\beta$, as $N \rightarrow \infty$. This is a consequence of the requirement that exponentially small energy gaps between the ground state of $H(t)$ and the first excited state, at some intermediate time, not lead to Landau-Zener transitions into excited states. The coefficients $\alpha$ and $\beta$ may be smaller than those in known classical algorithms, so there is still a possibility that an AQO algorithm may be more efficient than classical algorithms on some classes of problems.

### Tutorial Introduction

Returning to the tutorial, we start with the Hamiltonian:
$$ 
\mathcal{H(s)} = A(s) \sum_i{\sigma^x_i} + B(s) \left(\sum_i{a_i \sigma^z_i} + \sum_{i<j}{b_{ij} \sigma^z_i \sigma^z_j}\right)
$$
where $A(s)$ corresponds to an initial wave function with qubits in a superposition of up and down states, and $B(s)$ represents the problem the user wants to solve. The idea behind quantum annealing is that during the annealing cycle, you gradually decrease the initial state controlled by the transverse field and increase the final state. If this process is done slowly enough under adiabatic conditions (explain what adiabatic conditions are here), the system will end up in the ground state, which is the lowest possible energy state. In a programming sense, the Hamiltonian transforms into an objective function in a corresponding classical problem, involving the coefficients $A(s)$ and $B(s)$ and qubit variables $q_i$.

We will discuss these terms further, focusing on the problem transformed into qubit variables.

#### Annealing

The process of annealing metals inspired Simulated Annealing. To anneal a metal, you first heat it above a critical temperature, causing structural and property changes. Then, you carefully allow the metal to cool, retaining its newly-obtained properties.

In Simulated Annealing, a temperature variable simulates the heating process. You set it high and let the system "cool" as the algorithm runs.

The space of solutions defines an energy landscape, with the best solution being the lowest valley. Classical algorithms can only traverse this landscape, but quantum annealing can utilize quantum effects such as superposition and tunneling to potentially find better solutions.

Superposition allows quantum bits (qubits) to exist in multiple states simultaneously, enabling the exploration of many solutions at once. Tunneling allows qubits to pass through energy barriers rather than going over them, which can help escape local minima and find the global minimum more efficiently.

To formulate a problem for the quantum computer, we first specify an objective function that gives an energy value as a function of some variables.

Then the solution is an assignment of values to the variables. The lower the energy, the better the solution. Here are two cases: sometimes any low-energy solution is acceptable, sometimes only optimal solutions are acceptable.

Quantum annealing uses quantum physics to find low-energy solutions with high probability.

#### Programming Model

**Qubit ($q_i$)**: A quantum bit that participates in the annealing cycle and settles into one of two possible final states {0, 1}.

**Coupler ($q_i, q_j$)**: A physical device that allows one qubit to influence another qubit. The coupler creates an interaction between qubits, which can be used to encode problem constraints or relationships between variables.

**Weight ($a_i$)**: A real-valued constant associated with each qubit. The weight influences the qubit's tendency to collapse into one of its two possible final states (0 or 1). It represents the linear term in the Hamiltonian and is controlled by the programmer to encode the problem's objective function.

**Strength ($b_{ij}$)**: A real-valued constant associated with the interaction between two qubits (couplers). The strength determines the magnitude and nature (ferromagnetic or antiferromagnetic) of the interaction between qubits. It represents the quadratic term in the Hamiltonian and is also controlled by the programmer to encode the problem's constraints.

The system samples from the $q_i$ that minimize the objective function:
$$
Obj(a_i, b_{ij}; q_i) = \sum_i a_i q_i + \sum_{ij} b_{ij} q_i q_j
$$
The goal is to set $a_i$ and $b_{ij}$ so that when the machine calculates the objective function, it finds the lowest energy with a particular qubit solution. By appropriately setting $a_i$ and $b_{ij}$, we aim to influence the machine to find the lowest energy solution for the objective function.

## Binary Quadratic Model (BQM)

### QUBO 
QUBO stands for Quadratic Unconstrained Binary Optimization.

- **Quadratic**: The highest power of any variable in the objective function is two.
- **Unconstrained**: There are no constraints applied to the variables.
- **Binary**: The variables can only take values from the set {0, 1}.
- **Optimization**: The goal is to minimize or maximize an objective function.

QUBO
$$
Obj(c, a_i, b_{ij}; q_i) = c +  \sum_i{a_i q_i} + \sum_{i<j}{b_{ij} q_i q_j}
$$
Here q's are qubit variables - 0 and 1, instead of -1 and 1

a's and b's are adjustable constants

## Integer Partition Problem
The most important aspect of QUBO modeling is mapping the variables in the modeling object to binary (0/1 or -1/+1) variables. The integer partition problem is a simple and easy-to-understand example.

### Problem Definition
The integer partition problem is defined as:
Determine whether a set of N integers $a_1, ..., a_N$ can be partitioned into two subsets A and B such that the sum of the elements in each subset is equal.
For example:
{1, 5, 6} -> A = {1, 5}, B = {6}
In the example above, the sum of the elements in the two subsets A and B is equal to 6, so the set can be partitioned.

### Transforming into a Combinatorial Optimization Problem
In the previous QUBO examples, the variables used were 0 or 1. However, they can also be -1 or +1, which is then called the Ising model. When to use 0/1 and when to use -1/+1 will be explained with examples later.
In this problem, we use the labels of the two subsets as -1/+1 variables.
$$
x_i = \begin{cases}
-1, & \text{if the } i\text{th integer belongs to A} \\
1, & \text{if the } i\text{th integer belongs to B}
\end{cases}
$$
Our optimization goal becomes minimizing the squared difference of the sums of the two subsets. The objective function can be defined as:
$$
Obj(a_1,...,a_N) = (a_1 x_1 + a_2 x_2 + ... + a_N x_N)^2, \quad x_i \in \{-1, 1\}^N
$$

### Example for Objective Function with Target Set {1, 5, 6}

This example is referenced from [this article](https://blog.csdn.net/gangshen1993/article/details/127594967).

#### Objective Function
The objective function for the integer partition problem is defined as:
$$
Obj(a_1, a_2, a_3) = (1 \times x_1 + 5 \times x_2 + 6 \times x_3)^2, \quad x_i \in \{-1, 1\}^N
$$

#### Enumeration of Results

| \(a_1 = 1\) | \(a_2 = 5\) | \(a_3 = 6\) | \(Obj\) | Subset A | Subset B | Can be Separated |
|-------------|-------------|-------------|--------|----------|----------|------------------|
| -1          | -1          | -1          | 144    | {1, 5, 6} | {}       | No               |
| -1          | -1          | 1           | 0      | {1, 5}    | {6}      | Yes              |
| -1          | 1           | -1          | 4      | {1, 6}    | {5}      | No               |
| -1          | 1           | 1           | 100    | {1}       | {5, 6}   | No               |
| 1           | -1          | -1          | 100    | {5, 6}    | {1}      | No               |
| 1           | -1          | 1           | 4      | {5}       | {1, 6}   | No               |
| 1           | 1           | -1          | 0      | {6}       | {1, 5}   | Yes              |
| 1           | 1           | 1           | 144    | {}        | {1, 5, 6}| No               |

We could see when the Obj function reaches value 0, we could get the proper separated results.

- The objective function \(Obj\) is calculated as \((a_1 x_1 + a_2 x_2 + a_3 x_3)^2\).
- Subset A includes elements where \(x_i = -1\).
- Subset B includes elements where \(x_i = 1\).
- The "Can be Separated" column indicates whether the set can be partitioned into two subsets with equal sums.

Expanding the polynomial:
$$
Obj(a_1, a_2, a_3) 
= (x_1 + 5x_2 + 6x_3)^2
$$
$$
= x_1^2 + 25x_2^2 + 36x_3^2 + 10x_1x_2 + 12x_1x_3 + 60x_2x_3
$$

Since $x_i^2 = 1 $ for $x_i \in \{-1, 1\}$, we can simplify:
$$
= 1 + 25 + 36 + 10x_1x_2 + 12x_1x_3 + 60x_2x_3
$$
$$
= 62 + 10x_1x_2 + 12x_1x_3 + 60x_2x_3
$$

Now, let's rewrite the objective function in matrix form. The quadratic form of the objective function can be represented as:
$$
Obj = \mathbf{x}^T \mathbf{Q} \mathbf{x} + \mathbf{c}^T \mathbf{x} + \text{constant}
$$

Where:
$$
\mathbf{x} = \begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix}
$$
- $\mathbf{Q}$ is the matrix of quadratic coefficients

- $\mathbf{c}$ is the vector of linear coefficients

- The constant term is the sum of the squared terms

For our function:
$$
Obj = 62 + 10x_1x_2 + 12x_1x_3 + 60x_2x_3
$$

The matrix $\mathbf{Q}$ and vector $\mathbf{c}$ are:
$$
\mathbf{Q} = \begin{pmatrix}
0 & 5 & 6 \\
5 & 0 & 30 \\
6 & 30 & 0
\end{pmatrix}
$$

$$
\mathbf{c} = \begin{pmatrix}
0 \\
0 \\
0
\end{pmatrix}
$$

So the objective function in matrix form is:
$$
Obj = \mathbf{x}^T \mathbf{Q} \mathbf{x} + 62
$$
### Integer Partition Problem Implementation

The integer partition problem can be implemented in a Jupyter notebook. The notebook `integer_partition.py` demonstrates how to set up and solve the problem using the QUBO formulation.

In the notebook, we:

1. Define the objective function.
2. Compile the model.
3. Convert the model to a Binary Quadratic Model
4. Enumerate possible solutions and verify the results.

