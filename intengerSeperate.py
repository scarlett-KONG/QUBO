import pyqubo
import neal

# Create an array of variables 'x' with shape (3) and type 'SPIN'
# 'SPIN' means the target variables take values from {-1, 1}.
# If the target variables need to take values from {0, 1}, set vartype to 'BINARY'.
x = pyqubo.Array.create('x', shape=(3), vartype='SPIN')

# Define the objective function
objective_function = (1 * x[0] + 5 * x[1] + 6 * x[2]) ** 2

# Compile the model
model = objective_function.compile()

# Convert the model to a Binary Quadratic Model (BQM)
bqm = model.to_bqm()

print("We can convert the BQM to Ising or QUBO format")
print(bqm.to_ising())

# Use the Simulated Annealing Sampler from neal to sample from the BQM
sa = neal.SimulatedAnnealingSampler()
sampleset = sa.sample(bqm, num_reads=10)

# Decode the sampleset to get the samples
samples = model.decode_sampleset(sampleset)

# Find the best sample with the minimum energy
best_sample = min(samples, key=lambda s: s.energy)

print("During solving, pyqubo internally converts the Ising model to QUBO (0 or 1), so the output results are 0 or 1")
print(best_sample.sample)

'''
Output
We can convert the BQM to Ising or QUBO format
({'x[2]': np.float64(0.0), 'x[1]': np.float64(0.0), 'x[0]': np.float64(0.0)}, {('x[1]', 'x[2]'): np.float64(60.0), ('x[0]', 'x[2]'): np.float64(12.0), ('x[0]', 'x[1]'): np.float64(10.0)}, np.float64(62.0))
During solving, pyqubo internally converts the Ising model to QUBO (0 or 1), so the output results are 0 or 1
{'x[2]': 1, 'x[1]': 0, 'x[0]': 0}
'''