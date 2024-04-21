#!/usr/bin/env python3

"""
SecRules CRS Parser
-----------------------------------------------

Copyright (C) 2017 Felipe Zipitria <felipe.zipitria@owasp.org>

This program is free software; you can redistribute it and/or
modify it under the terms of the Apache License 2.0.

"""

import sys
import argparse
from textx.metamodel import metamodel_from_file, metamodel_from_str
from textx.exceptions import TextXSyntaxError
import json
from .resources import get_model

class SecRuleSyntaxError(Exception):
    def __str__(self) -> str:
        return f'SecRulesError: [SecRuleSyntaxError] line={self.args[0]}, col={self.args[1]}, message={self.args[2]}'
def process_rules(files, verbose=False, debug=False):
    """Parse our rule files with the provided parser"""
    models = []
    template = get_model()
    modsec_mm = metamodel_from_file(template, memoization=True, debug=debug)
    # Register test processor
    modsec_mm.register_obj_processors({"SecRule": secrule_id_processor})
    # Make sure we don't have an empty list of files
    if files == []:
        return models
    for rule_file in files:
        if verbose:
            print("Processing file %s:" % rule_file)
        try:
            model = modsec_mm.model_from_file(rule_file)
        except TextXSyntaxError as e:
            model = {
                "file": rule_file,
                "line": e.line,
                "col": e.col,
                "message": e.message,
            }
        models.append(model)
    return models


def secrule_id_processor(rule):
    """Processor for each rule, if needed"""
    pass


def get_rule_id(rule):
    """Gets rule ID. Only for a given SecAction or SecRule"""
    if rule.__class__.__name__ == "SecRule" or rule.__class__.__name__ == "SecAction":
        for action in rule.actions:
            if action.id:
                return action.id
    return 0


def get_rule_regex(rule):
    """Gets the regex. Only for a given SecAction or SecRule"""
    if rule.__class__.__name__ == "SecRule":
        output = {}
        if rule.operator.rx is not None:
            for action in rule.actions:
                if action.id:
                    if action.id in output.keys():
                        output[action.id].append(rule.operator.rx)
                    else:
                        output[action.id] = [rule.operator.rx]
                    return output
        return None


def get_correctness(files, models):
    """Checks the correctness of a given rules file"""

    for file_index in range(0, len(files)):
        if isinstance(models[file_index], dict):
            e = models[file_index]
            raise SecRuleSyntaxError(e['line'], e['col'], e['message'])
        else:
            continue


def process_from_str(str, verbose=False, debug=False):
    """Parse SecLanguage from string"""
    models = []
    template = get_model()
    modsec_mm = metamodel_from_file(template, memoization=True, debug=debug)
    # Register test processor
    modsec_mm.register_obj_processors({"SecRule": secrule_id_processor})
    # Make sure we don't have an empty list of files
    try:
        model = modsec_mm.model_from_str(str)
    except TextXSyntaxError as e:
        model = {
            "line": e.line,
            "col": e.col,
            "message": e.message,
        }
    return model
