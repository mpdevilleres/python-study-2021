import csv
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values


def main():
    values = []
    with open('covid_19_data.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for r in reader:
            try:
                values.append((
                    datetime.strptime(r[1].split(' ')[0], '%m/%d/%Y'),
                    r[2],
                    r[3],
                    datetime.strptime(r[4].split(' ')[0], '%m/%d/%Y'),
                    r[5],
                    r[6],
                    r[7]
                ))
            except:
                pass

    conn = psycopg2.connect(
        host="localhost",
        database="internal",
        user="postgres",
        password="postgres"
    )

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO public.covid_case (
        date_observed, province, region, date_updated, confirmed_count, death_count, recovered_count
        ) VALUES (%s)
        """,
                ...(100, "abc'def"))

    execute_values(
        cur,
        """
        INSERT INTO public.covid_case (
        date_observed, province, region, date_updated, confirmed_count, death_count, recovered_count
        ) VALUES %s
        """,
        values)

    # cur.commit()


if __name__ == '__main__':
    main()
