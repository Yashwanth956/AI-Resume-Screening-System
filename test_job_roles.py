from resume_parser.job_roles import JOB_ROLES


print("========== AVAILABLE JOB ROLES ==========")

for role, skills in JOB_ROLES.items():

    print("\nRole:", role)

    print("Skills:", skills)

print("\n==========================================")
print("Total Roles:", len(JOB_ROLES))