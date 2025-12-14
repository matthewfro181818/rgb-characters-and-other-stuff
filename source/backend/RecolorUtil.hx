package backend;

import flixel.FlxSprite;
import openfl.display.BitmapData;
import openfl.geom.Rectangle;
import openfl.geom.Point;

class RecolorUtil
{
    public static function recolor(
        sprite:FlxSprite,
        map:Map<Int, Int>
    ):Void
    {
        if (sprite == null || sprite.pixels == null || map == null)
            return;

        var src:BitmapData = sprite.pixels.clone();
        var rect = src.rect;

        for (from in map.keys())
        {
            src.threshold(
                src, rect, new Point(),
                "==",
                from,
                map.get(from),
                0xFFFFFFFF,
                false
            );
        }

        sprite.pixels = src;
        sprite.dirty = true;
        sprite.graphic.persist = true;
    }
}
