
import os
import hashlib
import jinja2

template_loader = jinja2.FileSystemLoader(searchpath="./resources_sql")
template_env = jinja2.Environment(loader=template_loader)


def template_retrieval(client, sql_file, **kwargs):
    sql = template_env.get_template(sql_file).render(**kwargs)
    output_df = client.query(sql, location="asia-east1").to_dataframe()
    if len(output_df) == 0:
        os.makedirs("errors", exist_ok=True)
        output_name = hashlib.sha256(sql.encode("utf-8")).hexdigest()
        with open("errors/" + output_name + ".sql", "w") as f:
            f.write(sql)
    return output_df

def retrieve_kol_post_time(
    platform: str, start_week: int, end_week: int, zh_country_name: str, project : str, client
):
    """
    Retrieve KOL post time
    """
   
    start_week = start_week - 6 # need to minus 6 for past post time 

    return template_retrieval(
        client,
        f"post_time_{platform}.sql",
        platform=platform,
        start_week=start_week,
        end_week=end_week,
        zh_country_name=zh_country_name,
        project= project,
    )