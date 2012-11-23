<?php

/**
 * Truetype to ASCII bitmap font conversion tool
 * requires FontBuilder bitmap font generator:
 * https://github.com/andryblack/fontbuilder
 *
 * @author  Andreas Goetz   <cpuidle@gmx.de>
 */

/**
 * Output debug info
 *
 * @param   var $var   Variable to dump
 */
function dump($var, $ret = false, $file = false)
{
	global $argv;

	if (is_array($var) || is_object($var))
		$var = print_r($var, 1);
	$var .= (count($argv) > 0 || $file) ? "\n" : "<br/>";

	if ($ret) return $var;
	echo $var;
}

/**
 * Convert XML + PNG font information to .py module
 */
function export_bitmap_font($img, $xml)
{
	/*
	$w = $xml->texture['width'];
	$height = $xml->texture['height'];
	*/

	$height = (int) $xml['height']+1;
	#dump($xml);die;

	// find SPACE character
	foreach ($xml->Char as $char)
	{
		/*
		 $id = $char['id'];
		$offset_x = $char['offset_x'];
		$offset_y = $char['offset_y'];
		$rect_x = $char['rect_x'];
		$rect_y = $char['rect_y'];
		$rect_w = $char['rect_w'];
		$rect_h = $char['rect_h'];
		$advance = $char['advance'];
		*/

		// <Char width="3" offset="0 10" rect="1 10 0 0" code=" "/>
		$id = (string) $char['code'];
		$width = (int) $char['width']+1;
	}
	
	// circumvent SPACE chacater
	$first_char = $xml->Char[0]['code'];
	if (REMOVE_SPACE && $first_char == " ")
		$first_char = $xml->Char[1]['code'];

	// header
	printf(<<<EOT
# Module fonts.%s_%d
name = "%s"
start_char = '%s'
end_char = '%s'
char_height = %d
space_width = %d
gap_width = %d

bitmaps = (

EOT
, $xml['family'], $height, $xml['family'], $first_char, $xml->Char[sizeof($xml->Char)-1]['code'], $height, 8, 0);

	$index = 0;
	$descriptors = array();
	$kerning = array();

	// put intp map
	#foreach ($xml->chars->char as $char)
	foreach ($xml->Char as $char)
	{
		/*
		 $id = $char['id'];
		$offset_x = $char['offset_x'];
		$offset_y = $char['offset_y'];
		$rect_x = $char['rect_x'];
		$rect_y = $char['rect_y'];
		$rect_w = $char['rect_w'];
		$rect_h = $char['rect_h'];
		$advance = $char['advance'];
		*/

		// <Char width="3" offset="0 10" rect="1 10 0 0" code=" "/>
		$id = (string) $char['code'];
		$width = (int) $char['width']+1;
		list($offset_x, $offset_y) = preg_split('/ /', $char['offset']);
		list($rect_x, $rect_y, $rect_w, $rect_h) = preg_split('/ /', $char['rect']);

		// TODO find out how to handle this correctly
		// cut first columns if offset is negative
		if ($offset_x < 0) {
			$rect_x -= $offset_x;
			$rect_w += $offset_x;
			$offset_x = 0;
		}
		$rect_w = min($width, $rect_w);
		$offset_x = max($offset_x, 0);
		$offset_y = max($offset_y, 0);
		
		// check plausibility
		if ($width < $rect_w) die(sprintf("Font %s, size %d, char %s: width < rect_w error (%d < %d)", $xml['family'], $height, $id, $width, $rect_w));
		if ($offset_x < 0) die(sprintf("Font %s, size %d, char %s: offset_x error (%d)", $xml['family'], $height, $id, $offset_x));
		if ($offset_y < 0) die(sprintf("Font %s, size %d, char %s: offset_y error (%d)", $xml['family'], $height, $id, $offset_y));
		#if ($id != "#") continue;
		
		// all non-SPACE characters
		if ($rect_w > 0 && $rect_h > 0 || !REMOVE_SPACE)
		{
/*
			// export character as PNG for debugging
			$target = imagecreate($rect_w, $rect_h);
			imagecopy($target, $img, 0, 0, $rect_x, $rect_y, $rect_w, $rect_h);
			imagepng($target, "_".$id.".png");
*/

			// put chacracter width and byte index in descriptors
			$descriptors[] = array($width, $index, $id);
				
			// increment index for following character
			$num_bytes = (int)($width/8) + (($width % 8 > 0) ? 1 : 0);
			$index += $height * $num_bytes;
			
			// character characteristics
			printf("    # @%d '%s' (%d pixels wide)\n", ord($id), $id, $width);

			// top rows
			for ($y=0; $y<$offset_y; $y++) {
				$l = INDENT;
				for ($i=0; $i<$num_bytes; $i++)
					$l .= '0x00, ';
				print($l." # \n");
			}

			// pixel to bytes conversion
			for ($y=0; $y<$rect_h; $y++) {
				$bits = 0;
				$x_idx = 0;
				$l = INDENT;
				$comment = '';
				
				// left gap
				for ($x=0; $x<$offset_x; $x++) {
					$comment .= '.';
				
					if (++$x_idx % 8 == 0) {
						$l .= '0x'.sprintf(FORMAT, $bits).', ';
						$bits = 0;
					}
				}
				
				// character
				for ($x=0; $x<$rect_w; $x++) {
					$rgb = imagecolorat($img, $rect_x + $x, $rect_y + $y);

					$transparency = ($rgb >> 24) & 0x7F;
					$comment .= $transparency ? ' ' : '*';

					if (!$transparency) $bits = $bits | (1 << (7 - ($x_idx) % 8));
					if (++$x_idx % 8 == 0) {
						$l .= '0x'.sprintf(FORMAT, $bits).', ';
						$bits = 0;
					}
				}

				// right gap
				for ($x=0; $x<$width-$offset_x-$rect_w; $x++) {
					$comment .= '.';
				
					if (++$x_idx % 8 == 0) {
						$l .= '0x'.sprintf(FORMAT, $bits).', ';
						$bits = 0;
					}
				}
				
				// remaining bits
				if ($width % 8 != 0) {
					$l .= '0x'.sprintf(FORMAT, $bits).', ';
				}
					
				print($l.' # '.$comment."\n");
			}

			// bottom rows
			for ($y=0; $y<$height-$offset_y-$rect_h; $y++) {
				$l = INDENT;
				for ($i=0; $i<$num_bytes; $i++)
					$l .= '0x00, ';
				print($l." # \n");
			}
			print("\n");

			// add kerning information
			$kerning[$id]['width'] = $width;
			foreach ($char->Kerning as $kern) {
				$kern_id = (string) $kern['id'];
				$delta   = (int) $kern['advance'];
				$kerning[$id][$kern_id] = $delta;
			}
		}
	}
	
	// footer - descriptors
	printf(<<<EOT
)

descriptors = (

EOT
	);

	foreach ($descriptors as $d) {
		vprintf("    (%d, %d), # %s\n", $d);
	}

	// footer - kerning
	printf(<<<EOT
)

kerning = (

EOT
	);

	// output kerning information
	foreach($kerning as $source =>$kern) {
		print("    (");
		foreach($kerning as $dest =>$foo) {
			$w = $kern['width'];
			#dump($kern);dump($dest);
			if (@$kern[$dest])
				$w += $kern[$dest];
			printf("%d,", $w);
		}
		printf("), # %s\n", $source);
	}

	printf(<<<EOT
)

kerning2 = {

EOT
	);
	
	// output kerning information
	foreach($kerning as $from_char => $kern) {
		if (count($kern) > 1) {
		printf("    '%s': {", addcslashes($from_char, "\\'"));
			foreach($kern as $to_char => $delta) {
				if ($to_char != 'width') {
					printf("'%s':%d, ", addcslashes($to_char, "\\'"), $delta);
				}
			}
			printf("}, \n", $from_char);
		}
	}

	printf(<<<EOT
}
	
# End of font

EOT
	);
}

define('FORMAT', '%02X');
define('INDENT', '    ');
define('REMOVE_SPACE', false);

// use -f to specify input folder
if (!($options = getopt('f::o::h::')) || @$options['h'])
	die('Usage: convert_font [-f=font data folder] [-o=output folder]');

$base = $options['f'];
if (strlen($base) && ($base[strlen($base)-1] != DIRECTORY_SEPARATOR)) $base .= DIRECTORY_SEPARATOR;

$output = $options['o'];
if (strlen($output) && ($output[strlen($output)-1] != DIRECTORY_SEPARATOR)) $output .= DIRECTORY_SEPARATOR;

foreach (glob("$base*.xml") as $file) {
	$path = pathinfo($file);
	$base = $path['dirname'].DIRECTORY_SEPARATOR.$path['filename'];
	#if ($path['filename'] != 'arial_regular_10') continue;
	
	$img = imagecreatefrompng($base.'.png');
	$xml = simplexml_load_file($base.'.xml');

	ob_start();
	export_bitmap_font($img, $xml);
	$contents = ob_get_contents();

	file_put_contents($output.$path['filename'].".py", $contents);
}

?>
