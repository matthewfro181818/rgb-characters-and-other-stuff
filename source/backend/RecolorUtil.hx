
package backend;

import flixel.FlxSprite;
import openfl.geom.ColorTransform;

class RecolorUtil
{
    public static function recolor(sprite:FlxSprite, map:Map<String, Map<String,String>>)
    {
        if (sprite == null || map == null) return;

        var pixels = sprite.pixels;
        if (pixels == null) return;

        pixels.lock();

        for (part in map.keys())
        {
            var swaps = map.get(part);
            for (fromHex in swaps.keys())
            {
                var toHex = swaps.get(fromHex);

                var from = Std.parseInt(fromHex.replace("#","0xFF"));
                var to   = Std.parseInt(toHex.replace("#","0xFF"));

                pixels.threshold(
                    pixels,
                    pixels.rect,
                    new openfl.geom.Point(),
                    "==",
                    from,
                    to,
                    0xFFFFFFFF,
                    true
                );
            }
        }

        pixels.unlock();
        sprite.dirty = true;
    }
}
