(function()
{
	Sidebar.prototype.addFencingPalette = function()
	{
		var w = 100;
		var h = 100;
		var s = 'strokeWidth=2;whiteSpace=wrap;html=1;shape=mxgraph.fencing.';
		var s2 = mxConstants.STYLE_VERTICAL_LABEL_POSITION + '=bottom;' + mxConstants.STYLE_VERTICAL_ALIGN + '=top;html=1;strokeWidth=2;shape=mxgraph.fencing.';
		var s3 = mxConstants.STYLE_VERTICAL_LABEL_POSITION + '=bottom;' + mxConstants.STYLE_VERTICAL_ALIGN + '=top;html=1;strokeWidth=2;shape=';
		var gn = 'mxgraph.fencing';
		var dt = '';
		
		this.addPaletteFunctions('fencing', 'Fencing', true,
		[
			this.createVertexTemplateEntry(s2 + 'fence', w, h, '', 'Fence', null, null, this.getTagsForStencil(gn, 'fence', dt).join(' ')),

			this.createVertexTemplateEntry(s2 + 'gate', w, h, '', 'Gate', null, null, this.getTagsForStencil(gn, 'gate', dt).join(' ')),

			this.createVertexTemplateEntry(s2 + 'building', w, h, '', 'Building', null, null, this.getTagsForStencil(gn, 'building', dt).join(' '))
			
		]);
	};

})();
