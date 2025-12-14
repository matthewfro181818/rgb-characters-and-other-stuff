package backend;

import haxe.Json;
import sys.io.File;
import sys.FileSystem;

class RecolorPreset
{
    public static function load(path:String):Dynamic
    {
        if (!FileSystem.exists(path))
            return null;

        try
        {
            return Json.parse(File.getContent(path));
        }
        catch (e)
        {
            trace('[RecolorPreset] Failed to load ' + path);
            return null;
        }
    }
}
