# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class SmMenuRenamerRule(models.Model):
    _name = "sm.menu.renamer.rule"
    _description = "Menu Renamer Rule"
    _order = "menu_id"

    active = fields.Boolean(default=True)
    menu_id = fields.Many2one(
        "ir.ui.menu",
        string="Menu Item",
        required=True,
        ondelete="cascade",
        help="The exact menu item to rename. The full menu path is shown, "
             "so two menus with the same name cannot be mixed up.",
    )
    new_name = fields.Char(required=True, help="Replacement name, e.g. 'Penjualan'.")
    lang = fields.Selection(
        selection=lambda self: self.env["res.lang"].get_installed(),
        string="Language",
        help="Apply the rename only in this language. Leave empty for all languages.",
    )

    @api.model
    @tools.ormcache("lang")
    def _get_rename_map(self, lang):
        rules = self.sudo().search_read(
            ["|", ("lang", "=", lang), ("lang", "=", False)],
            ["menu_id", "new_name", "lang"],
        )
        # language specific rules win over generic ones
        rules.sort(key=lambda r: bool(r["lang"]))
        return {r["menu_id"][0]: r["new_name"] for r in rules}

    def _clear_menu_cache(self):
        self.env.registry.clear_cache()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._clear_menu_cache()
        return records

    def write(self, vals):
        result = super().write(vals)
        self._clear_menu_cache()
        return result

    def unlink(self):
        result = super().unlink()
        self._clear_menu_cache()
        return result


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    def _sm_menu_rename_map(self):
        if "sm.menu.renamer.rule" not in self.env:
            return {}
        return self.env["sm.menu.renamer.rule"]._get_rename_map(
            self.env.lang or "en_US"
        )

    @api.model
    def load_menus(self, debug):
        menus = super().load_menus(debug)
        mapping = self._sm_menu_rename_map()
        if mapping:
            # super() result is ormcached and shared: copy, never mutate
            menus = dict(menus)
            for menu_id, new_name in mapping.items():
                if menu_id in menus:
                    menus[menu_id] = {**menus[menu_id], "name": new_name}
        return menus
