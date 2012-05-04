/**
 * Copyright 2012 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @author benvanik@google.com (Ben Vanik)
 */

goog.provide('cube.start');

goog.require('cube.CubeDemo');
goog.require('gf');
goog.require('gf.LaunchOptions');
goog.require('goog.asserts');
goog.require('goog.dom.DomHelper');


/**
 * Starts the game client.
 * @param {string} uri Invoking URI.
 * @param {!Document} doc HTML document object.
 */
cube.start = function(uri, doc) {
  goog.asserts.assert(!gf.SERVER);

  // Create game
  var dom = new goog.dom.DomHelper(doc);
  var launchOptions = new gf.LaunchOptions(uri);
  var game = new cube.CubeDemo(launchOptions, dom);

  // HACK: debug root - useful for inspecting the game state
  if (goog.DEBUG) {
    goog.global['game_client'] = game;
  }
};


goog.exportSymbol('cube.start', cube.start);
