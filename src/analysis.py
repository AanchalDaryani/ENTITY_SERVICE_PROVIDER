from src.db_connection import get_connection
from src.generate_synthetic_data import (
    generate_entities,
    generate_service_providers,
    generate_relationship_dates
)
import random
from datetime import date, timedelta


def insert_entities():
    conn = get_connection()
    cursor = conn.cursor()

    # Generate 1000 entities
    entities = generate_entities(1000)

    for entity in entities:
        cursor.execute(
            "INSERT INTO entities (entity_name) VALUES (%s)",
            (entity,)
        )

    conn.commit()
    cursor.close()
    conn.close()



def insert_service_providers():
    conn = get_connection()
    cursor = conn.cursor()

    providers = generate_service_providers()

    for name, ptype in providers:
        cursor.execute(
            "INSERT INTO service_providers (provider_name, provider_type) VALUES (%s, %s)",
            (name, ptype)
        )

    conn.commit()
    cursor.close()
    conn.close()


def insert_relationships():
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch entities
    cursor.execute("SELECT entity_id FROM entities")
    entity_ids = [row[0] for row in cursor.fetchall()]

    # Fetch providers grouped by type
    cursor.execute("""
        SELECT provider_id, provider_type
        FROM service_providers
    """)
    providers = cursor.fetchall()

    providers_by_type = {
        "Auditor": [p[0] for p in providers if p[1] == "Auditor"],
        "Custodian": [p[0] for p in providers if p[1] == "Custodian"],
        "Administrator": [p[0] for p in providers if p[1] == "Administrator"],
    }

    # Choose ~6% of entities for overlap injection
    overlap_entities = set(
        random.sample(entity_ids, int(len(entity_ids) * 0.06))
    )

    for entity_id in entity_ids:
        assigned_types = {}

        # STEP 1: baseline — one provider per type
        for ptype, provider_list in providers_by_type.items():
            provider_id = random.choice(provider_list)
            start_date, end_date = generate_relationship_dates()

            cursor.execute(
                """
                INSERT INTO entity_provider_relationships
                (entity_id, provider_id, start_date, end_date)
                VALUES (%s, %s, %s, %s)
                """,
                (entity_id, provider_id, start_date, end_date)
            )

            assigned_types[ptype] = (provider_id, start_date, end_date)

        # STEP 2: missing provider (~25%)
        if random.random() < 0.25:
            missing_type = random.choice(list(assigned_types.keys()))

            cursor.execute(
                """
                DELETE FROM entity_provider_relationships
                WHERE relationship_id = (
                    SELECT relationship_id FROM (
                        SELECT r.relationship_id
                        FROM entity_provider_relationships r
                        JOIN service_providers sp
                          ON r.provider_id = sp.provider_id
                        WHERE r.entity_id = %s
                          AND sp.provider_type = %s
                        LIMIT 1
                    ) AS tmp
                )
                """,
                (entity_id, missing_type)
            )

        # STEP 3: overlapping providers (~6%)
        if entity_id in overlap_entities:
            overlap_type = random.choice(list(providers_by_type.keys()))

            provider_id = random.choice(providers_by_type[overlap_type])

            # Overlapping active dates
            overlap_start = date.today() - timedelta(days=200)
            overlap_end = date.today() + timedelta(days=400)

            cursor.execute(
                """
                INSERT INTO entity_provider_relationships
                (entity_id, provider_id, start_date, end_date)
                VALUES (%s, %s, %s, %s)
                """,
                (entity_id, provider_id, overlap_start, overlap_end)
            )

    conn.commit()
    cursor.close()
    conn.close()
