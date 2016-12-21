function element(tag, attributes, content, closing) {
    var $element = "";// returning string
    var iter;
    for (iter = 0; iter < tag.length; ++iter) {

        $element += "<" + tag[iter];

        for (var key in attributes[iter]) {
            if (attributes[iter].hasOwnProperty(key)) {
                //# adding an attribute to the tag[i]#
                $element += ( " " + key + "=\'" + attributes[iter][key] + "\'");
            }
        }

        $element += ">";
        $element += content[iter];
    }

    for (iter = tag.length - 1; iter > -1; --iter) {
        if (closing[iter]) {
            $element += "</" + tag[iter] + ">"
        }
    }

    return $element;
}
