Blockly.Blocks['phil'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Phil");
    this.setOutput(true, null);
    this.setColour(180);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['sarah'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Sarah");
    this.setOutput(true, null);
    this.setColour(180);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['says'] = {
  init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput();
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField(":   \"");
    this.appendDummyInput()
        .appendField("\"");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['prefix'] = {
  init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("")
        .appendField(new Blockly.FieldTextInput("default"), "NAME");
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['suffix'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput("default"), "NAME");
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['title'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("An Origin Story");
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['suffix_fixed'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("I was looking fly. ");
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['it_started_with'] = {
  init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("it started with");
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['a_tool'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("a tool");
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['stuck'] = {
  init: function() {
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField("I'm stuck waiting backstage when I notice");
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['suffix_mixed'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("this")
        .appendField(new Blockly.FieldTextInput("girl"), "noun");
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['mixx'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("he walks over, ")
        .appendField(new Blockly.FieldTextInput("stupid sweater"), "NAME")
        .appendField("and all");
    this.setOutput(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['start_says'] = {
  init: function() {
    this.appendValueInput("NAME")
        .setCheck(null);
    this.appendDummyInput();
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField(":   \"");
    this.appendDummyInput()
        .appendField("\"");
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['end_says'] = {
  init: function() {
    this.appendValueInput("hi")
        .setCheck(null);
    this.appendDummyInput();
    this.appendValueInput("NAME")
        .setCheck(null)
        .appendField(":   \"");
    this.appendDummyInput()
        .appendField("\"");
    this.setPreviousStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};