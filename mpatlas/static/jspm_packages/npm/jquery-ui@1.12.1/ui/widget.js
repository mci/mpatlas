/* */ 
"format cjs";
(function(process) {
  (function(factory) {
    if (typeof define === "function" && define.amd) {
      define(["jquery", "./version"], factory);
    } else {
      factory(jQuery);
    }
  }(function($) {
    var widgetUuid = 0;
    var widgetSlice = Array.prototype.slice;
    $.cleanData = (function(orig) {
      return function(elems) {
        var events,
            elem,
            i;
        for (i = 0; (elem = elems[i]) != null; i++) {
          try {
            events = $._data(elem, "events");
            if (events && events.remove) {
              $(elem).triggerHandler("remove");
            }
          } catch (e) {}
        }
        orig(elems);
      };
    })($.cleanData);
    $.widget = function(name, base, prototype) {
      var existingConstructor,
          constructor,
          basePrototype;
      var proxiedPrototype = {};
      var namespace = name.split(".")[0];
      name = name.split(".")[1];
      var fullName = namespace + "-" + name;
      if (!prototype) {
        prototype = base;
        base = $.Widget;
      }
      if ($.isArray(prototype)) {
        prototype = $.extend.apply(null, [{}].concat(prototype));
      }
      $.expr[":"][fullName.toLowerCase()] = function(elem) {
        return !!$.data(elem, fullName);
      };
      $[namespace] = $[namespace] || {};
      existingConstructor = $[namespace][name];
      constructor = $[namespace][name] = function(options, element) {
        if (!this._createWidget) {
          return new constructor(options, element);
        }
        if (arguments.length) {
          this._createWidget(options, element);
        }
      };
      $.extend(constructor, existingConstructor, {
        version: prototype.version,
        _proto: $.extend({}, prototype),
        _childConstructors: []
      });
      basePrototype = new base();
      basePrototype.options = $.widget.extend({}, basePrototype.options);
      $.each(prototype, function(prop, value) {
        if (!$.isFunction(value)) {
          proxiedPrototype[prop] = value;
          return;
        }
        proxiedPrototype[prop] = (function() {
          function _super() {
            return base.prototype[prop].apply(this, arguments);
          }
          function _superApply(args) {
            return base.prototype[prop].apply(this, args);
          }
          return function() {
            var __super = this._super;
            var __superApply = this._superApply;
            var returnValue;
            this._super = _super;
            this._superApply = _superApply;
            returnValue = value.apply(this, arguments);
            this._super = __super;
            this._superApply = __superApply;
            return returnValue;
          };
        })();
      });
      constructor.prototype = $.widget.extend(basePrototype, {widgetEventPrefix: existingConstructor ? (basePrototype.widgetEventPrefix || name) : name}, proxiedPrototype, {
        constructor: constructor,
        namespace: namespace,
        widgetName: name,
        widgetFullName: fullName
      });
      if (existingConstructor) {
        $.each(existingConstructor._childConstructors, function(i, child) {
          var childPrototype = child.prototype;
          $.widget(childPrototype.namespace + "." + childPrototype.widgetName, constructor, child._proto);
        });
        delete existingConstructor._childConstructors;
      } else {
        base._childConstructors.push(constructor);
      }
      $.widget.bridge(name, constructor);
      return constructor;
    };
    $.widget.extend = function(target) {
      var input = widgetSlice.call(arguments, 1);
      var inputIndex = 0;
      var inputLength = input.length;
      var key;
      var value;
      for (; inputIndex < inputLength; inputIndex++) {
        for (key in input[inputIndex]) {
          value = input[inputIndex][key];
          if (input[inputIndex].hasOwnProperty(key) && value !== undefined) {
            if ($.isPlainObject(value)) {
              target[key] = $.isPlainObject(target[key]) ? $.widget.extend({}, target[key], value) : $.widget.extend({}, value);
            } else {
              target[key] = value;
            }
          }
        }
      }
      return target;
    };
    $.widget.bridge = function(name, object) {
      var fullName = object.prototype.widgetFullName || name;
      $.fn[name] = function(options) {
        var isMethodCall = typeof options === "string";
        var args = widgetSlice.call(arguments, 1);
        var returnValue = this;
        if (isMethodCall) {
          if (!this.length && options === "instance") {
            returnValue = undefined;
          } else {
            this.each(function() {
              var methodValue;
              var instance = $.data(this, fullName);
              if (options === "instance") {
                returnValue = instance;
                return false;
              }
              if (!instance) {
                return $.error("cannot call methods on " + name + " prior to initialization; " + "attempted to call method '" + options + "'");
              }
              if (!$.isFunction(instance[options]) || options.charAt(0) === "_") {
                return $.error("no such method '" + options + "' for " + name + " widget instance");
              }
              methodValue = instance[options].apply(instance, args);
              if (methodValue !== instance && methodValue !== undefined) {
                returnValue = methodValue && methodValue.jquery ? returnValue.pushStack(methodValue.get()) : methodValue;
                return false;
              }
            });
          }
        } else {
          if (args.length) {
            options = $.widget.extend.apply(null, [options].concat(args));
          }
          this.each(function() {
            var instance = $.data(this, fullName);
            if (instance) {
              instance.option(options || {});
              if (instance._init) {
                instance._init();
              }
            } else {
              $.data(this, fullName, new object(options, this));
            }
          });
        }
        return returnValue;
      };
    };
    $.Widget = function() {};
    $.Widget._childConstructors = [];
    $.Widget.prototype = {
      widgetName: "widget",
      widgetEventPrefix: "",
      defaultElement: "<div>",
      options: {
        classes: {},
        disabled: false,
        create: null
      },
      _createWidget: function(options, element) {
        element = $(element || this.defaultElement || this)[0];
        this.element = $(element);
        this.uuid = widgetUuid++;
        this.eventNamespace = "." + this.widgetName + this.uuid;
        this.bindings = $();
        this.hoverable = $();
        this.focusable = $();
        this.classesElementLookup = {};
        if (element !== this) {
          $.data(element, this.widgetFullName, this);
          this._on(true, this.element, {remove: function(event) {
              if (event.target === element) {
                this.destroy();
              }
            }});
          this.document = $(element.style ? element.ownerDocument : element.document || element);
          this.window = $(this.document[0].defaultView || this.document[0].parentWindow);
        }
        this.options = $.widget.extend({}, this.options, this._getCreateOptions(), options);
        this._create();
        if (this.options.disabled) {
          this._setOptionDisabled(this.options.disabled);
        }
        this._trigger("create", null, this._getCreateEventData());
        this._init();
      },
      _getCreateOptions: function() {
        return {};
      },
      _getCreateEventData: $.noop,
      _create: $.noop,
      _init: $.noop,
      destroy: function() {
        var that = this;
        this._destroy();
        $.each(this.classesElementLookup, function(key, value) {
          that._removeClass(value, key);
        });
        this.element.off(this.eventNamespace).removeData(this.widgetFullName);
        this.widget().off(this.eventNamespace).removeAttr("aria-disabled");
        this.bindings.off(this.eventNamespace);
      },
      _destroy: $.noop,
      widget: function() {
        return this.element;
      },
      option: function(key, value) {
        var options = key;
        var parts;
        var curOption;
        var i;
        if (arguments.length === 0) {
          return $.widget.extend({}, this.options);
        }
        if (typeof key === "string") {
          options = {};
          parts = key.split(".");
          key = parts.shift();
          if (parts.length) {
            curOption = options[key] = $.widget.extend({}, this.options[key]);
            for (i = 0; i < parts.length - 1; i++) {
              curOption[parts[i]] = curOption[parts[i]] || {};
              curOption = curOption[parts[i]];
            }
            key = parts.pop();
            if (arguments.length === 1) {
              return curOption[key] === undefined ? null : curOption[key];
            }
            curOption[key] = value;
          } else {
            if (arguments.length === 1) {
              return this.options[key] === undefined ? null : this.options[key];
            }
            options[key] = value;
          }
        }
        this._setOptions(options);
        return this;
      },
      _setOptions: function(options) {
        var key;
        for (key in options) {
          this._setOption(key, options[key]);
        }
        return this;
      },
      _setOption: function(key, value) {
        if (key === "classes") {
          this._setOptionClasses(value);
        }
        this.options[key] = value;
        if (key === "disabled") {
          this._setOptionDisabled(value);
        }
        return this;
      },
      _setOptionClasses: function(value) {
        var classKey,
            elements,
            currentElements;
        for (classKey in value) {
          currentElements = this.classesElementLookup[classKey];
          if (value[classKey] === this.options.classes[classKey] || !currentElements || !currentElements.length) {
            continue;
          }
          elements = $(currentElements.get());
          this._removeClass(currentElements, classKey);
          elements.addClass(this._classes({
            element: elements,
            keys: classKey,
            classes: value,
            add: true
          }));
        }
      },
      _setOptionDisabled: function(value) {
        this._toggleClass(this.widget(), this.widgetFullName + "-disabled", null, !!value);
        if (value) {
          this._removeClass(this.hoverable, null, "ui-state-hover");
          this._removeClass(this.focusable, null, "ui-state-focus");
        }
      },
      enable: function() {
        return this._setOptions({disabled: false});
      },
      disable: function() {
        return this._setOptions({disabled: true});
      },
      _classes: function(options) {
        var full = [];
        var that = this;
        options = $.extend({
          element: this.element,
          classes: this.options.classes || {}
        }, options);
        function processClassString(classes, checkOption) {
          var current,
              i;
          for (i = 0; i < classes.length; i++) {
            current = that.classesElementLookup[classes[i]] || $();
            if (options.add) {
              current = $($.unique(current.get().concat(options.element.get())));
            } else {
              current = $(current.not(options.element).get());
            }
            that.classesElementLookup[classes[i]] = current;
            full.push(classes[i]);
            if (checkOption && options.classes[classes[i]]) {
              full.push(options.classes[classes[i]]);
            }
          }
        }
        this._on(options.element, {"remove": "_untrackClassesElement"});
        if (options.keys) {
          processClassString(options.keys.match(/\S+/g) || [], true);
        }
        if (options.extra) {
          processClassString(options.extra.match(/\S+/g) || []);
        }
        return full.join(" ");
      },
      _untrackClassesElement: function(event) {
        var that = this;
        $.each(that.classesElementLookup, function(key, value) {
          if ($.inArray(event.target, value) !== -1) {
            that.classesElementLookup[key] = $(value.not(event.target).get());
          }
        });
      },
      _removeClass: function(element, keys, extra) {
        return this._toggleClass(element, keys, extra, false);
      },
      _addClass: function(element, keys, extra) {
        return this._toggleClass(element, keys, extra, true);
      },
      _toggleClass: function(element, keys, extra, add) {
        add = (typeof add === "boolean") ? add : extra;
        var shift = (typeof element === "string" || element === null),
            options = {
              extra: shift ? keys : extra,
              keys: shift ? element : keys,
              element: shift ? this.element : element,
              add: add
            };
        options.element.toggleClass(this._classes(options), add);
        return this;
      },
      _on: function(suppressDisabledCheck, element, handlers) {
        var delegateElement;
        var instance = this;
        if (typeof suppressDisabledCheck !== "boolean") {
          handlers = element;
          element = suppressDisabledCheck;
          suppressDisabledCheck = false;
        }
        if (!handlers) {
          handlers = element;
          element = this.element;
          delegateElement = this.widget();
        } else {
          element = delegateElement = $(element);
          this.bindings = this.bindings.add(element);
        }
        $.each(handlers, function(event, handler) {
          function handlerProxy() {
            if (!suppressDisabledCheck && (instance.options.disabled === true || $(this).hasClass("ui-state-disabled"))) {
              return;
            }
            return (typeof handler === "string" ? instance[handler] : handler).apply(instance, arguments);
          }
          if (typeof handler !== "string") {
            handlerProxy.guid = handler.guid = handler.guid || handlerProxy.guid || $.guid++;
          }
          var match = event.match(/^([\w:-]*)\s*(.*)$/);
          var eventName = match[1] + instance.eventNamespace;
          var selector = match[2];
          if (selector) {
            delegateElement.on(eventName, selector, handlerProxy);
          } else {
            element.on(eventName, handlerProxy);
          }
        });
      },
      _off: function(element, eventName) {
        eventName = (eventName || "").split(" ").join(this.eventNamespace + " ") + this.eventNamespace;
        element.off(eventName).off(eventName);
        this.bindings = $(this.bindings.not(element).get());
        this.focusable = $(this.focusable.not(element).get());
        this.hoverable = $(this.hoverable.not(element).get());
      },
      _delay: function(handler, delay) {
        function handlerProxy() {
          return (typeof handler === "string" ? instance[handler] : handler).apply(instance, arguments);
        }
        var instance = this;
        return setTimeout(handlerProxy, delay || 0);
      },
      _hoverable: function(element) {
        this.hoverable = this.hoverable.add(element);
        this._on(element, {
          mouseenter: function(event) {
            this._addClass($(event.currentTarget), null, "ui-state-hover");
          },
          mouseleave: function(event) {
            this._removeClass($(event.currentTarget), null, "ui-state-hover");
          }
        });
      },
      _focusable: function(element) {
        this.focusable = this.focusable.add(element);
        this._on(element, {
          focusin: function(event) {
            this._addClass($(event.currentTarget), null, "ui-state-focus");
          },
          focusout: function(event) {
            this._removeClass($(event.currentTarget), null, "ui-state-focus");
          }
        });
      },
      _trigger: function(type, event, data) {
        var prop,
            orig;
        var callback = this.options[type];
        data = data || {};
        event = $.Event(event);
        event.type = (type === this.widgetEventPrefix ? type : this.widgetEventPrefix + type).toLowerCase();
        event.target = this.element[0];
        orig = event.originalEvent;
        if (orig) {
          for (prop in orig) {
            if (!(prop in event)) {
              event[prop] = orig[prop];
            }
          }
        }
        this.element.trigger(event, data);
        return !($.isFunction(callback) && callback.apply(this.element[0], [event].concat(data)) === false || event.isDefaultPrevented());
      }
    };
    $.each({
      show: "fadeIn",
      hide: "fadeOut"
    }, function(method, defaultEffect) {
      $.Widget.prototype["_" + method] = function(element, options, callback) {
        if (typeof options === "string") {
          options = {effect: options};
        }
        var hasOptions;
        var effectName = !options ? method : options === true || typeof options === "number" ? defaultEffect : options.effect || defaultEffect;
        options = options || {};
        if (typeof options === "number") {
          options = {duration: options};
        }
        hasOptions = !$.isEmptyObject(options);
        options.complete = callback;
        if (options.delay) {
          element.delay(options.delay);
        }
        if (hasOptions && $.effects && $.effects.effect[effectName]) {
          element[method](options);
        } else if (effectName !== method && element[effectName]) {
          element[effectName](options.duration, options.easing, callback);
        } else {
          element.queue(function(next) {
            $(this)[method]();
            if (callback) {
              callback.call(element[0]);
            }
            next();
          });
        }
      };
    });
    return $.widget;
  }));
})(require('process'));
