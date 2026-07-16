# -*- coding: utf-8 -*-
{
    "name": "Menu Item Renamer",
    "version": "15.0.1.0.0",
    "category": "Extra Tools",
    "summary": "Rename any menu item without writing a single line of code, per language, without touching the original menus.",
    "description": """
Menu Item Renamer
=================

Rename any menu item from a simple configuration screen. No code, no XML,
no Studio. Pick the menu, type the new name, refresh the browser.

* Rename apps and menu items anywhere in the backend
* Pick the exact menu from a list, no ambiguity between menus with the same name
* Language aware: rename a menu in one language without touching the others
* Works with standard and custom modules
* Dedicated "Menu Renamer Manager" access group
* Rules are applied on the fly, original menus are never modified
    """,
    "author": "Steven Marp",
    "website": "https://apps.odoo.com/apps/modules/browse?author=Steven Marp",
    "license": "OPL-1",
    "images": [
        "static/description/banner.gif",
        "static/description/icon.png",
        "static/description/menu_renamer_01_rule_config.png",
        "static/description/menu_renamer_02_menu_result.png",
    ],
    "depends": ["base", "web"],
    "data": [
        "security/menu_renamer_security.xml",
        "security/ir.model.access.csv",
        "views/menu_renamer_rule_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "price": 35.00,
    "currency": "USD",
}
