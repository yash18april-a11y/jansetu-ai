"""One-time additive profile migration. Back up the database before running."""
import os
from sqlalchemy import inspect, text
from app import create_app
from app.extensions import db

COLUMNS = {
    'full_name': 'VARCHAR(120)',
    'district': 'VARCHAR(120)',
    'gender': 'VARCHAR(40)',
    'education_level': 'VARCHAR(80)',
    'employment_status': 'VARCHAR(80)',
    'household_size': 'INTEGER',
    'social_category': 'VARCHAR(60)',
    'disability_status': 'BOOLEAN',
}

def main():
    if os.getenv('CONFIRM_PROFILE_V2_MIGRATION') != 'YES':
        raise RuntimeError('Set CONFIRM_PROFILE_V2_MIGRATION=YES after backing up your database')
    app = create_app()
    with app.app_context():
        if db.engine.dialect.name not in {'postgresql', 'mysql'}:
            raise RuntimeError('Only PostgreSQL and MySQL are supported')
        existing = {c['name'] for c in inspect(db.engine).get_columns('citizen_profile')}
        with db.engine.begin() as connection:
            for name, column_type in COLUMNS.items():
                if name not in existing:
                    connection.execute(text(f'ALTER TABLE citizen_profile ADD COLUMN {name} {column_type}'))
                    print('Added:', name)
                else:
                    print('Already present:', name)
        print('Profile V2 migration complete')

if __name__ == '__main__':
    main()
