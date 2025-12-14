package backend;

import haxe.Json;
import sys.io.File;
import sys.FileSystem;

class RecolorPreset
{
    public static function load(path:String):Map<Int, Int>
    {
        var map = new Map<Int, Int>();
        if (!FileSystem.exists(path)) return map;

        var json = Json.parse(File.getContent(path));
        for (k in Reflect.fields(json))
        {
            var e = Reflect.field(json, k);
            map.set(hex(e.from), hex(e.to));
        }
        return map;
    }

    static function hex(s:String):Int
    {
        return Std.parseInt("0xFF" + s.substr(1));
    }
}
