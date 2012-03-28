#!/usr/bin/python

# Copyright 2012 Google Inc. All Rights Reserved.

"""Tests for the project module.
"""

__author__ = 'benvanik@google.com (Ben Vanik)'


import unittest2

from project import *


class RuleTest(unittest2.TestCase):
  """Behavioral tests of the Rule type."""

  def testRuleNames(self):
    with self.assertRaises(NameError):
      Rule(None)
    with self.assertRaises(NameError):
      Rule('')
    with self.assertRaises(NameError):
      Rule(' ')
    with self.assertRaises(NameError):
      Rule(' a')
    with self.assertRaises(NameError):
      Rule('a ')
    with self.assertRaises(NameError):
      Rule(' a ')
    with self.assertRaises(NameError):
      Rule('a\n')
    with self.assertRaises(NameError):
      Rule('a\t')
    with self.assertRaises(NameError):
      Rule('a b')
    with self.assertRaises(NameError):
      Rule(':a')
    rule = Rule('a')
    self.assertEqual(rule.name, 'a')
    self.assertEqual(rule.full_name, ':a')
    Rule('\u0CA_\u0CA')

  def testRuleSrcs(self):
    rule = Rule('r')
    self.assertEqual(len(rule.srcs), 0)

    srcs = ['a', 'b', ':c']
    rule = Rule('r', srcs=srcs)
    self.assertEqual(len(rule.srcs), 3)
    self.assertIsNot(rule.srcs, srcs)
    srcs[0] = 'x'
    self.assertEqual(rule.srcs[0], 'a')

    srcs = 'a'
    rule = Rule('r', srcs=srcs)
    self.assertEqual(len(rule.srcs), 1)
    self.assertEqual(rule.srcs[0], 'a')

    rule = Rule('r', srcs=None)
    rule = Rule('r', srcs='')
    self.assertEqual(len(rule.srcs), 0)
    with self.assertRaises(TypeError):
      Rule('r', srcs={})
    with self.assertRaises(TypeError):
      Rule('r', srcs=[None])
    with self.assertRaises(TypeError):
      Rule('r', srcs=[''])
    with self.assertRaises(TypeError):
      Rule('r', srcs=[{}])
    with self.assertRaises(NameError):
      Rule('r', srcs=' a')
    with self.assertRaises(NameError):
      Rule('r', srcs='a ')
    with self.assertRaises(NameError):
      Rule('r', srcs=' a ')

  def testRuleDeps(self):
    rule = Rule('r')
    self.assertEqual(len(rule.deps), 0)

    deps = [':a', ':b', ':c']
    rule = Rule('r', deps=deps)
    self.assertEqual(len(rule.deps), 3)
    self.assertIsNot(rule.deps, deps)
    deps[0] = 'x'
    self.assertEqual(rule.deps[0], ':a')

    deps = ':a'
    rule = Rule('r', deps=deps)
    self.assertEqual(len(rule.deps), 1)
    self.assertEqual(rule.deps[0], ':a')

    rule = Rule('r', deps=None)
    rule = Rule('r', deps='')
    self.assertEqual(len(rule.deps), 0)
    with self.assertRaises(TypeError):
      Rule('r', deps={})
    with self.assertRaises(TypeError):
      Rule('r', deps=[None])
    with self.assertRaises(TypeError):
      Rule('r', deps=[''])
    with self.assertRaises(TypeError):
      Rule('r', deps={})
    with self.assertRaises(NameError):
      Rule('r', deps=' a')
    with self.assertRaises(NameError):
      Rule('r', deps='a ')
    with self.assertRaises(NameError):
      Rule('r', deps=' a ')

  def testRuleCacheKey(self):
    rule1 = Rule('r1')
    rule1_key = rule1.compute_cache_key()
    self.assertIsNotNone(rule1_key)
    self.assertGreater(len(rule1_key), 0)
    self.assertEqual(rule1_key, rule1.compute_cache_key())
    rule1.srcs.append('a')
    self.assertNotEqual(rule1_key, rule1.compute_cache_key())

    rule1 = Rule('r1')
    rule2 = Rule('r1')
    self.assertEqual(rule1.compute_cache_key(), rule2.compute_cache_key())
    rule1 = Rule('r1')
    rule2 = Rule('r2')
    self.assertNotEqual(rule1.compute_cache_key(), rule2.compute_cache_key())

    rule1 = Rule('r1', srcs='a')
    rule2 = Rule('r1', srcs='a')
    self.assertEqual(rule1.compute_cache_key(), rule2.compute_cache_key())
    rule1 = Rule('r1', srcs='a')
    rule2 = Rule('r1', srcs='b')
    self.assertNotEqual(rule1.compute_cache_key(), rule2.compute_cache_key())
    rule1 = Rule('r1', deps=':a')
    rule2 = Rule('r1', deps=':a')
    self.assertEqual(rule1.compute_cache_key(), rule2.compute_cache_key())
    rule1 = Rule('r1', deps=':a')
    rule2 = Rule('r1', deps=':b')
    self.assertNotEqual(rule1.compute_cache_key(), rule2.compute_cache_key())
    rule1 = Rule('r1', srcs='a', deps=':a')
    rule2 = Rule('r1', srcs='a', deps=':a')
    self.assertEqual(rule1.compute_cache_key(), rule2.compute_cache_key())
    rule1 = Rule('r1', srcs='a', deps=':a')
    rule2 = Rule('r1', srcs='b', deps=':b')
    self.assertNotEqual(rule1.compute_cache_key(), rule2.compute_cache_key())


class ProjectTest(unittest2.TestCase):
  """Behavioral tests of Project rule handling."""

  def testEmptyProject(self):
    project = Project()
    self.assertIsNone(project.get_rule(':a'))
    self.assertEqual(len(project.rules_list()), 0)
    self.assertEqual(len(list(project.rules_iter())), 0)

  def testProjectName(self):
    project = Project()
    self.assertNotEqual(len(project.name), 0)
    project = Project(project_name='a')
    self.assertEqual(project.name, 'a')

  def testAddRule(self):
    project = Project()
    rule_a = Rule('a')
    rule_b = Rule('b')
    self.assertIsNone(project.get_rule(':a'))
    project.add_rule(rule_a)
    self.assertEqual(project.get_rule(':a'), rule_a)
    self.assertEqual(len(project.rules_list()), 1)
    self.assertEqual(len(list(project.rules_iter())), 1)
    self.assertEqual(project.rules_list()[0], rule_a)
    self.assertEqual(list(project.rules_iter())[0], rule_a)
    self.assertIsNone(project.get_rule(':b'))
    project.add_rule(rule_b)
    self.assertEqual(project.get_rule(':b'), rule_b)
    self.assertEqual(len(project.rules_list()), 2)
    self.assertEqual(len(list(project.rules_iter())), 2)

  def testAddRules(self):
    project = Project()
    rule_a = Rule('a')
    rule_b = Rule('b')
    rules = [rule_a, rule_b]
    self.assertIsNone(project.get_rule(':a'))
    self.assertIsNone(project.get_rule(':b'))
    self.assertEqual(len(project.rules_list()), 0)
    project.add_rules(rules)
    self.assertEqual(len(project.rules_list()), 2)
    self.assertEqual(len(list(project.rules_iter())), 2)
    self.assertIsNot(project.rules_list(), rules)
    self.assertEqual(project.get_rule(':a'), rule_a)
    self.assertEqual(project.get_rule(':b'), rule_b)

  def testGetRule(self):
    project = Project()
    rule = Rule('a')
    project.add_rule(rule)

    self.assertIs(project.get_rule(':a'), rule)
    with self.assertRaises(NameError):
      project.get_rule('a')

    self.assertIsNone(project.get_rule(':x'))
