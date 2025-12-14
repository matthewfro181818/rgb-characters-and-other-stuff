package backend;

import openfl.display.BitmapData;

class RecolorAuto
{
    public static function findFlatColors(bmp:BitmapData):Array<Int>
    {
        var found = new Map<Int, Bool>();

        for (x in 0...bmp.width)
        for (y in 0...bmp.height)
        {
            var c = bmp.getPixel32(x, y);
            if ((c >> 24) > 0xF0)
                found.set(c, true);
        }

        return [for (k in found.keys()) k];
    }
}
