function element(tags, attributes, contents, closings) {
    var $element = "";// returning string
    var iter;
    for (iter = 0; iter < tags.length; ++iter) {

        $element += "<" + tags[iter];

        for (var key in attributes[iter]) {
            if (attributes[iter].hasOwnProperty(key)) {
                //# adding an attribute to the tags[i]#
                $element += ( " " + key + "=\'" + attributes[iter][key] + "\'");
            }
        }

        $element += ">";
        $element += contents[iter];
    }

    for (iter = tags.length - 1; iter > -1; --iter) {
        if (closings[iter]) {
            $element += "</" + tags[iter] + ">"
        }
    }

    return $element;
}
