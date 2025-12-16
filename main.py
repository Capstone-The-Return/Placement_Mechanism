import numpy as np

# 1. Ορισμός των Υπηρεσιών (Service Graph Nodes)
# Format: 'Name': [CPU_req, RAM_req]
services = {
    'A. Web Server': [2, 2],
    'B. Backend API': [3, 3],
    'C. Database':    [3, 4]
}

# 2. Ορισμός Διαθέσιμων Servers (Simulated Infrastructure)
# Φτιάχνουμε 3 εικονικούς servers με διαφορετικά χαρακτηριστικά
# για να δούμε πώς θα συμπεριφερθεί ο αλγόριθμος.
servers = {
    'Server_1 (Small)':  {'cpu': 4,  'ram': 4},   # Ιδανικός για μικρά
    'Server_2 (Medium)': {'cpu': 6,  'ram': 8},   # Ισορροπημένος
    'Server_3 (Large)':  {'cpu': 8, 'ram': 16}    # Πολλή μνήμη (καλός για DB)
}

def cosine_similarity(vec_a, vec_b):
    """
    Υπολογισμός Cosine Similarity μεταξύ δύο διανυσμάτων.
    Formula: (A . B) / (||A|| * ||B||)
    """
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot_product / (norm_a * norm_b)

def placement_algorithm(services, servers):
    print("--- Έναρξη Διαδικασίας Τοποθέτησης (Best-Fit with Cosine Sim) ---\n")
    
    results = {}

    for service_name, reqs in services.items():
        req_cpu, req_ram = reqs
        req_vector = np.array([req_cpu, req_ram])
        
        best_server = None
        max_score = -1
        
        print(f"Αναζήτηση Server για: {service_name} (CPU: {req_cpu}, RAM: {req_ram})")
        
        # Έλεγχος κάθε Server
        for server_name, specs in servers.items():
            avail_cpu = specs['cpu']
            avail_ram = specs['ram']
            
            # Βήμα 1: Έλεγχος αν χωράει (Hard Constraint) 
            if avail_cpu >= req_cpu and avail_ram >= req_ram:
                avail_vector = np.array([avail_cpu, avail_ram])
                
                # Βήμα 2: Υπολογισμός Cosine Similarity [cite: 12]
                score = cosine_similarity(req_vector, avail_vector)
                
                print(f"  -> Έλεγχος {server_name}: Διαθέσιμα [C:{avail_cpu}, R:{avail_ram}] -> Score: {score:.4f}")
                
                # Βήμα 3: Επιλογή Best-Fit (Μεγαλύτερο Score) [cite: 11]
                if score > max_score:
                    max_score = score
                    best_server = server_name
            else:
                print(f"  -> {server_name}: Ανεπαρκείς πόροι.")

        # Ανάθεση και Ενημέρωση Πόρων
        if best_server:
            print(f"  ==> ΕΠΙΛΟΓΗ: {best_server} (Score: {max_score:.4f})\n")
            results[service_name] = best_server
            
            # Μείωση των διαθέσιμων πόρων στον server που επιλέχθηκε
            servers[best_server]['cpu'] -= req_cpu
            servers[best_server]['ram'] -= req_ram
        else:
            print(f"  ==> ΑΠΟΤΥΧΙΑ: Δεν βρέθηκε κατάλληλος server!\n")
            results[service_name] = "None"

    return results, servers

# Εκτέλεση
final_placement, final_state = placement_algorithm(services, servers)

print("--- Τελική Τοποθέτηση ---")
for srv, host in final_placement.items():
    print(f"{srv} --> {host}")

print("\n--- Εναπομείναντες Πόροι ---")
for s, specs in final_state.items():
    print(f"{s}: CPU={specs['cpu']}, RAM={specs['ram']}")