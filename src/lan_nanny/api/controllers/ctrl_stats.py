"""
    Bookmarky Api
    Controller
    Stats
    /stats

"""
from flask import Blueprint, jsonify, Response

from lan_nanny.api.stats import entity_stats
from lan_nanny.api.collects.tags import Tags
from lan_nanny.api.utils import auth
from lan_nanny.api.utils import glow

ctrl_stats = Blueprint("stats", __name__, url_prefix="/stats")


@auth.auth_request
@ctrl_stats.route("/top-tags")
def top_tags() -> Response:
    """Get the Tags which have the most relationships.
    @todo: restrict this to user_id
    """
    RESULTS = 20
    data = {
        "info": "Bookmarky",
        "objects": []
    }
    sql = """
        SELECT tag_id, COUNT(tag_id) AS tag_count
        FROM bookmark_tags
        GROUP BY tag_id
        ORDER BY tag_count DESC
        LIMIT %s
    """
    #         -- LIMIT %s;
    # glow.db["cursor"].execute(sql, (RESULTS,))
    glow.db["cursor"].execute(sql, (RESULTS,))
    rows = glow.db["cursor"].fetchall()
    tag_ids = _get_ids(rows)
    tag_col = Tags()
    tags_select = tag_col.get_by_ids(tag_ids)
    tags_select = tag_col.make_json(tags_select)
    tags = []
    for tag in tags_select:
        tags.append(_get_tag_stat(tag, rows))
    data["objects"] = sorted(tags, key=lambda x: x["metas"]["count"])
    data["objects"].reverse()

    return jsonify(data)


@auth.auth_request
@ctrl_stats.route("/entity-counts")
def entity_counts() -> Response:
    """Get all entity counts"""
    data = {
        "info": "Entity Counts",
        "entities": {}
    }
    data["entities"] = entity_stats.get_all_entity_counts()
    return jsonify(data)


def _get_tag_stat(tag: dict, tag_stats: list) -> dict:
    """
    """
    for stat in tag_stats:
        if stat[0] == tag["id"]:
            tag["metas"] = {
                "count": stat[1]
            }
            return tag
    return tag


def _get_ids(rows) -> list:
    """Generate a list of Tag IDs from a result set."""
    ret_ids = []
    for row in rows:
        ret_ids.append(row[0])
    return ret_ids

# End File: politeauthroity/bookmark-apiy/src/bookmarky/api/controllers/ctrl_stats.py
