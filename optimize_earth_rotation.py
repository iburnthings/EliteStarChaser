import numpy as np
from scipy.optimize import minimize

# Known target in-game coordinates for multiple stars (X_target, Y_target, Z_target)
targets = [
    (-322.6875, -212.4375, 194.59375),  # Target coordinates for Polaris
    (72.15625, -66.875, -232.5),   # Bellatrix
    (25.21875, 25899.96875, -20.90625), #Sag A*
    (-1111.5625, 65269.75, -134.21875), #Beagle Point
    (-9530.5, 19808.125, -910.28125 ), #Colonia
    # Add more target coordinates as needed
]
# Observable RA and Dec, with distance from Earth (D) for each star in celestial coordinates
# Define RA as (hours, minutes, seconds) and Dec as (degrees, minutes, seconds)
stars = [
    {"RA": (3, 47, 38.553), "Dec": (89, 27, 7.710), "Distance": 432.58},   # Polaris
    {"RA": (5, 27, 48.177), "Dec": (6, 23, 24.701), "Distance": 252.46},   # Bellatrix    
    {"RA": (17, 45, 40.055), "Dec": (-29, 0, 28.398), "Distance": 25899.99},    # Sag A*
    {"RA": (17, 48, 22.957), "Dec": (-28, 9, 46.890), "Distance": 65279.35},    # Beagle Point
    {"RA": (18, 46, 40.866), "Dec": (-7, 31, 17.408), "Distance": 22000.47},    # Colonia
    # Add more stars as needed, must be in same order as target coordinates
]

# Function to convert RA from hours, minutes, and seconds to radians
def ra_to_radians(hours, minutes, seconds):
    total_hours = hours + minutes / 60 + seconds / 3600
    return np.radians(total_hours * 15)  # Convert to degrees (1 hr = 15 degrees), then to radians

# Function to convert Dec from degrees, minutes, and seconds to radians
def dec_to_radians(degrees, minutes, seconds):
    total_degrees = abs(degrees) + minutes / 60 + seconds / 3600
    if degrees < 0:
        total_degrees = -total_degrees
    return np.radians(total_degrees)

# Step 1: Convert RA, Dec, Distance to Cartesian coordinates for a star
def celestial_to_cartesian(RA, Dec, D):
    X = D * np.cos(Dec) * np.cos(RA)
    Y = D * np.cos(Dec) * np.sin(RA)
    Z = D * np.sin(Dec)
    return X, Y, Z

# Step 2: Apply rotations given angles alpha, beta, gamma
def apply_rotations(X, Y, Z, alpha, beta, gamma):
    # Rotation around Z-axis
    X_prime = X * np.cos(alpha) - Y * np.sin(alpha)
    Y_prime = X * np.sin(alpha) + Y * np.cos(alpha)
    Z_prime = Z

    # Rotation around Y-axis
    X_double_prime = X_prime * np.cos(beta) + Z_prime * np.sin(beta)
    Y_double_prime = Y_prime
    Z_double_prime = -X_prime * np.sin(beta) + Z_prime * np.cos(beta)

    # Rotation around X-axis
    X_triple_prime = X_double_prime
    Y_triple_prime = Y_double_prime * np.cos(gamma) - Z_double_prime * np.sin(gamma)
    Z_triple_prime = Y_double_prime * np.sin(gamma) + Z_double_prime * np.cos(gamma)

    return X_triple_prime, Y_triple_prime, Z_triple_prime

# Step 3: Define the loss function for multiple stars
def loss_function(angles):
    alpha, beta, gamma = angles
    total_error = 0.0
    for star, (X_target, Y_target, Z_target) in zip(stars, targets):
        # Convert RA, Dec from (hours, minutes, seconds) and (degrees, minutes, seconds) to radians
        RA = ra_to_radians(*star["RA"])
        Dec = dec_to_radians(*star["Dec"])
        # Convert to Cartesian using distance
        X, Y, Z = celestial_to_cartesian(RA, Dec, star["Distance"])
        # Apply rotations
        X_transformed, Y_transformed, Z_transformed = apply_rotations(X, Y, Z, alpha, beta, gamma)
        # Calculate error for this star
        error = np.sqrt((X_transformed - X_target)**2 + (Y_transformed - Y_target)**2 + (Z_transformed - Z_target)**2)
        total_error += error
    return total_error

# Initial guess for the angles (in radians)
initial_angles = [0.0, 0.0, 0.0]

# Step 4: Use the optimizer to find the best angles
result = minimize(loss_function, initial_angles, method='BFGS')
alpha_opt, beta_opt, gamma_opt = result.x

# Output the optimized angles
print("Optimized Angles (in degrees):")
print("Alpha:", np.degrees(alpha_opt))
print("Beta:", np.degrees(beta_opt))
print("Gamma:", np.degrees(gamma_opt))

# Apply the optimized rotations and print the transformed coordinates for each star
print("Transformed Coordinates for each star:")
for star, (X_target, Y_target, Z_target) in zip(stars, targets):
    RA = ra_to_radians(*star["RA"])
    Dec = dec_to_radians(*star["Dec"])
    X, Y, Z = celestial_to_cartesian(RA, Dec, star["Distance"])
    X_final, Y_final, Z_final = apply_rotations(X, Y, Z, alpha_opt, beta_opt, gamma_opt)
    print(f"Target: ({X_target}, {Y_target}, {Z_target})")
    print(f"Transformed: ({X_final}, {Y_final}, {Z_final})\n")
