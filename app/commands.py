# -*- coding: utf-8 -*-
from app import app
import click
from flask import Blueprint
from app.models.models import User, UserProfile, AdminSettings

mod = Blueprint('commands', __name__)


@mod.cli.command('create-admin-settings')
def create_admin_settings():
    user = User.query.filter_by(email="germes04141@gmail.com").first()
    user_profile = UserProfile \
        .query.join(User.profile) \
        .filter(User.id == user.id).first()

    #  Start ID 1
    admin_settings_payload_id_1 = AdminSettings.query.filter_by(id=1).first()
    if admin_settings_payload_id_1 is None:
        admin_settings_payload_id_1 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Start 1 hónap ára",
            settings_type="number",
            settings_value="5"
        )
        admin_settings_payload_id_1.id = 1
        admin_settings_payload_id_1.db_post()
    #  End ID 1

    #  Start ID 2
    admin_settings_payload_id_2 = AdminSettings.query.filter_by(id=2).first()
    if admin_settings_payload_id_2 is None:
        admin_settings_payload_id_2 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Basic 1 hónap ára",
            settings_type="number",
            settings_value="50"
        )
        admin_settings_payload_id_2.id = 2
        admin_settings_payload_id_2.db_post()
    #  End ID 2

    #  Start ID 3
    admin_settings_payload_id_3 = AdminSettings.query.filter_by(id=3).first()
    if admin_settings_payload_id_3 is None:
        admin_settings_payload_id_3 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Premium 1 hónap ára",
            settings_type="number",
            settings_value="75"
        )
        admin_settings_payload_id_3.id = 3
        admin_settings_payload_id_3.db_post()
    #  End ID 3

    #  Start ID 4
    admin_settings_payload_id_4 = AdminSettings.query.filter_by(id=4).first()
    if admin_settings_payload_id_4 is None:
        admin_settings_payload_id_4 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Start 3 hónap ára",
            settings_type="number",
            settings_value="15"
        )
        admin_settings_payload_id_4.id = 4
        admin_settings_payload_id_4.db_post()
    #  End ID 4

    #  Start ID 5
    admin_settings_payload_id_5 = AdminSettings.query.filter_by(id=5).first()
    if admin_settings_payload_id_5 is None:
        admin_settings_payload_id_5 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Basic 3 hónap ára",
            settings_type="number",
            settings_value="100"
        )
        admin_settings_payload_id_5.id = 5
        admin_settings_payload_id_5.db_post()
    #  End ID 5

    #  Start ID 6
    admin_settings_payload_id_6 = AdminSettings.query.filter_by(id=6).first()
    if admin_settings_payload_id_6 is None:
        admin_settings_payload_id_6 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Premium 3 hónap ára",
            settings_type="number",
            settings_value="150"
        )
        admin_settings_payload_id_6.id = 6
        admin_settings_payload_id_6.db_post()
    #  End ID 6

    #  Start ID 7
    admin_settings_payload_id_7 = AdminSettings.query.filter_by(id=7).first()
    if admin_settings_payload_id_7 is None:
        admin_settings_payload_id_7 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Start 1 év ára",
            settings_type="number",
            settings_value="50"
        )
        admin_settings_payload_id_7.id = 7
        admin_settings_payload_id_7.db_post()
    #  End ID 7

    #  Start ID 8
    admin_settings_payload_id_8 = AdminSettings.query.filter_by(id=8).first()
    if admin_settings_payload_id_8 is None:
        admin_settings_payload_id_8 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Basic 1 év ára",
            settings_type="number",
            settings_value="350"
        )
        admin_settings_payload_id_8.id = 8
        admin_settings_payload_id_8.db_post()
    #  End ID 8

    #  Start ID 9
    admin_settings_payload_id_9 = AdminSettings.query.filter_by(id=9).first()
    if admin_settings_payload_id_9 is None:
        admin_settings_payload_id_9 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Premium 1 év ára",
            settings_type="number",
            settings_value="500"
        )
        admin_settings_payload_id_9.id = 9
        admin_settings_payload_id_9.db_post()
    #  End ID 9

    #  Start ID 10
    admin_settings_payload_id_10 = AdminSettings.query.filter_by(id=10).first()
    if admin_settings_payload_id_10 is None:
        admin_settings_payload_id_10 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Start feladható hírdetések száma",
            settings_type="number",
            settings_value="1"
        )
        admin_settings_payload_id_10.id = 10
        admin_settings_payload_id_10.db_post()
    #  End ID 10

    #  Start ID 11
    admin_settings_payload_id_11 = AdminSettings.query.filter_by(id=11).first()
    if admin_settings_payload_id_11 is None:
        admin_settings_payload_id_11 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Basic feladható hírdetések száma",
            settings_type="number",
            settings_value="10"
        )
        admin_settings_payload_id_11.id = 11
        admin_settings_payload_id_11.db_post()
    #  End ID 11

    #  Start ID 12
    admin_settings_payload_id_12 = AdminSettings.query.filter_by(id=12).first()
    if admin_settings_payload_id_12 is None:
        admin_settings_payload_id_12 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Premium feladható hírdetések száma",
            settings_type="number",
            settings_value="0"
        )
        admin_settings_payload_id_12.id = 12
        admin_settings_payload_id_12.db_post()
    #  End ID 12

    #  Start ID 13
    admin_settings_payload_id_13 = AdminSettings.query.filter_by(id=13).first()
    if admin_settings_payload_id_13 is None:
        admin_settings_payload_id_13 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Start chat kapcsolat száma",
            settings_type="number",
            settings_value="50"
        )
        admin_settings_payload_id_13.id = 13
        admin_settings_payload_id_13.db_post()
    #  End ID 13

    #  Start ID 14
    admin_settings_payload_id_14 = AdminSettings.query.filter_by(id=14).first()
    if admin_settings_payload_id_14 is None:
        admin_settings_payload_id_14 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Basic chat kapcsolat száma",
            settings_type="number",
            settings_value="250"
        )
        admin_settings_payload_id_14.id = 14
        admin_settings_payload_id_14.db_post()
    #  End ID 14

    #  Start ID 15
    admin_settings_payload_id_15 = AdminSettings.query.filter_by(id=15).first()
    if admin_settings_payload_id_15 is None:
        admin_settings_payload_id_15 = AdminSettings(
            settings_user_id=user.id,
            settings_user_name=user_profile.username,
            settings_name="ANLI Premium chat kapcsolat száma",
            settings_type="number",
            settings_value="0"
        )
        admin_settings_payload_id_15.id = 15
        admin_settings_payload_id_15.db_post()
    #  End ID 15
