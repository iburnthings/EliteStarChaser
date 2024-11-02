import numpy as np

# Optimized angles (already determined)
alpha_opt = np.radians(-318.00443284172417)  # Convert to radians
beta_opt = np.radians(228.3296119276629)     # Convert to radians
gamma_opt = np.radians(226.6974094318606)    # Convert to radians

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

# Convert RA, Dec, Distance to Cartesian coordinates for a star
def celestial_to_cartesian(RA, Dec, D):
    X = D * np.cos(Dec) * np.cos(RA)
    Y = D * np.cos(Dec) * np.sin(RA)
    Z = D * np.sin(Dec)
    return X, Y, Z

# Apply rotations using optimized angles alpha, beta, gamma
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

# Input new star's celestial coordinates (RA: hours, minutes, seconds; Dec: degrees, minutes, seconds; Distance in light-years)
new_star = {
    "RA": (5, 6, 27.23), # example RA in hours, minutes, seconds
    "Dec": (4, 1, 26.0), # example Dec in degrees, minutes, seconds
    "Distance": 645.09,   # example distance in light-years     
}
    
# Step 1: Convert RA and Dec to radians
RA = ra_to_radians(*new_star["RA"])
Dec = dec_to_radians(*new_star["Dec"])

# Step 2: Convert celestial coordinates to Cartesian coordinates
X, Y, Z = celestial_to_cartesian(RA, Dec, new_star["Distance"])

# Step 3: Apply the optimized rotations
X_final, Y_final, Z_final = apply_rotations(X, Y, Z, alpha_opt, beta_opt, gamma_opt)

# Output the transformed coordinates
print("Transformed Coordinates for the new star:")
print(f"X: {X_final}")
print(f"Y: {Y_final}")
print(f"Z: {Z_final}")
