define(
	[
		'//cdn.sencha.com/ext/gpl/4.1.1/ext-all'
	],
	function () {
		MPALayersWindow = {
		
			load: function (map) {
				this.map = map;
				
				Ext.define('MPALayersWindow.dataModel', {
					extend: 'Ext.data.Model',
					fields: [
						'id', 'name', 'color', 'layer'
					],
					idProperty: 'id'
				});
				
				this.selModel = Ext.create("Ext.selection.CheckboxModel", {
					mode: 'SIMPLE',
					checkOnly: true,
					listeners: {
						selectionChange: function (sm, records) {
							MPALayersWindow.updateMapLayerVisibility(sm, records);
						}
					}
				});

				// create the Store for Overlay Layers
				this.overlayStore = Ext.create('Ext.data.Store', {
					model: this.dataModel,
					listeners: {
						datachanged: function () {
							MPALayersWindow.syncMapLayerVisibility();					
						}
					}
				});
				
				renderSwatch = function (val, meta, record) {
						var color = record.get('color');
						if (!color) {
						return '';
						} else {
						var id = (record && record.id) ? record.id : Ext.id();
						return '<img id="legendSwatch' + id + '" src="' + Ext.BLANK_IMAGE_URL + '" style="border:1px  #999999 solid;width:13px;height:13px;' + (Ext.isIE ? 'margin-top:1px;' : '') + 'background-color:' + color + ';margin-top:5px;" />';
						}
				};
				
				this.overlayGrid = Ext.create('Ext.grid.Panel', {
					selModel: this.selModel,
					sortableColumns: false,
					forceFit: true,
					columns: [
						{
							id: 'name',
							dataIndex: 'name',
							width: 215
						},
						{
							id: 'swatch',
							dataIndex: 'color',
							width: 20,
							renderer: renderSwatch
						}
					],
					rowLines: false,
					columnLines: false,
					hideHeaders: true,
					viewConfig: {
						trackOver: false,
						stripeRows: false
					},
					store: this.overlayStore
				});
				
				this.window = Ext.create('Ext.window.Window', {
					width: 250,
					//x: 600,
					//y: 125,
					layout: 'fit',
					title: 'Map Layers',
					id: 'MPALayers',
					collapsible: true,
					closable: false,
					closeAction: 'hide',

					/*
					tbar: [
						{
							xtype: 'button',
							text: '- Remove All Filters',
							handler: function () {
								MPAFiltersWindow.clearFilters();
							}
						}
					],
					*/
					
					items: [
						this.overlayGrid
					],
					listeners: {
						'show': function () {
							MPALayersWindow.loadLayers();
						}
					}
				});
				
				this.window.show();
				this.window.hide();
				this.window.alignTo('leafletmap', 'bl-bl', [35, -30]);
			},
			
			loadLayers: function () {
				var data = [], rec = null, opts = null;
				
				// load the overlay Layers
				var lyr = null, lyrs = this.map.overlayLayers;
				for (lyr in lyrs) {
					opts = lyrs[lyr].options;
					rec = {
						id: opts.id,
						name: lyr,
						color: opts.color,
						layer: lyrs[lyr]
					};
					data.push(rec);
				}
				
				// Add the filter layer
				if (MPAFiltersWindow.isFiltered()) {
					rec = {
						id: 'filter',
						name: 'Filtered MPAs'
					};
					data.push(rec);			
				}
		
				this.overlayStore.loadData(data);
				
				lyr = null;
				lyrs = this.map.bgLayers;
				data = [];
				for (lyr in lyrs) {
					opts = lyrs[lyr].options;
					rec = {
						id: opts.id,
						name: lyr,
						color: opts.color,
						layer: lyrs[lyr]
					};
					data.push(rec);
				}
		
				
			},
			
			updateMapLayerVisibility: function () {
				var k = 0, len = this.overlayStore.getCount();
				var rec = null, lyr = null, sel = null, id = null;
				var selected = this.selModel.selected;
				for (k = 0; k < len; k++) {
					rec = this.overlayStore.getAt(k);
					if (rec) {
						lyr = rec.get('layer');
						sel = selected.get(rec.id);
						id = rec.get('id');
						if (id !== 'filter') {
							if (sel) {
								this.map.map.addLayer(lyr, false);
							} else {
								this.map.map.removeLayer(lyr);
							}
						} else if (MPAFiltersWindow.isFiltered()) {
							if (sel) {
								this.map.clusterer.show();
							} else {
								this.map.clusterer.hide();
							}
						}
					}				
				}
			},
			
			syncMapLayerVisibility: function () {
				var k = 0, len = this.overlayStore.getCount();
				var rec = null, lyr = null, id = null;
				for (k = 0; k < len; k++) {
					rec = this.overlayStore.getAt(k);
					if (rec) {
						id = rec.get('id');
						lyr = rec.get('layer');
						if (id !== 'filter') {
							if (lyr._map) {
								this.selModel.select(rec, true, true);
							} else {
								this.selModel.deselect(rec, true);						
							}
						} else {
							if (MPAFiltersWindow.isFiltered()) {
								this.selModel.select(rec, true, true);
							} else {
								this.selModel.deselect(rec, true);
							}
						}
					}
				}		
			},
		
			showLayer: function (sm, rec, idx) {
				var map = this.map.map;
				var lyr = rec.get('layer');
				map.addLayer(lyr, false);
			},
		
			hideLayer: function (sm, rec, idx) {
				var map = this.map.map;
				var lyr = rec.get('layer');
				map.removeLayer(lyr);
			}
			
		}
	}
)