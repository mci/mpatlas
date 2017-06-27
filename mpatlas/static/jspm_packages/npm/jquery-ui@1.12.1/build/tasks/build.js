/* */ 
(function(Buffer) {
  module.exports = function(grunt) {
    "use strict";
    grunt.registerTask("clean", function() {
      require('rimraf').sync("dist");
    });
    grunt.registerTask("asciilint", function() {
      var valid = true,
          files = grunt.file.expand({filter: "isFile"}, "ui/*.js");
      files.forEach(function(filename) {
        var i,
            c,
            text = grunt.file.read(filename);
        if (/\x0d\x0a/.test(text)) {
          grunt.log.error(filename + ": Incorrect line endings (\\r\\n)");
          valid = false;
        }
        if (text.length !== Buffer.byteLength(text, "utf8")) {
          grunt.log.error(filename + ": Non-ASCII characters detected:");
          for (i = 0; i < text.length; i++) {
            c = text.charCodeAt(i);
            if (c > 127) {
              grunt.log.error("- position " + i + ": " + c);
              grunt.log.error("-- " + text.substring(i - 20, i + 20));
              break;
            }
          }
          valid = false;
        }
      });
      if (valid) {
        grunt.log.ok(files.length + " files lint free.");
      }
      return valid;
    });
  };
})(require('buffer').Buffer);
