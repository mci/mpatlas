define(
	[
		'//cdn.sencha.com/ext/gpl/4.1.1/ext-all'
	],
	function () {
		console.log(Ext);
		MPAFiltersWindow = {
			markers: [],
			filtered: false,
			points: null,
			filters: null,
			mapFilters: null,
			
			load: function (map) {
				this.map = map;
				
				this.points = new Ext.util.MixedCollection(false, function (o) {
					return o.properties.mpa_id;
				});
				this.filters = new Ext.util.MixedCollection();
				this.mapFilters = new Ext.util.MixedCollection();
				
				this.loadFilterTree();		
				this.loadSelectionGrid();
				this.loadPanels();
		
				this.btnAddFilter = Ext.create('Ext.Button', {
					text: 'Add Filter',
					disabled: true,
					handler: MPAFiltersWindow.addFilter,
					style: 'margin:10px;',
					scope: MPAFiltersWindow
				});
				
				this.window = Ext.create('Ext.window.Window', {
					height: 325,
					width: 500,
					modal: true,
					title: 'Add Map Filter',
					id: 'MPAFilters',
					closeAction: 'hide',
					layout: {
						type: 'border',
						padding: 0
					},
					items: [
						{
							region: 'west',
							title: 'Select A Filter',
							width: 200,
							items: this.treePanel
						},
						{
							region: 'center',
							items: this.selectionPanel
						}
					],
					buttons: [
						this.btnAddFilter
					]
				});
				
				this.points.addAll(mpa_points.features);
		
				this.applyQSFilter();	
			},
			
			loadFilterTree: function () {
				
				Ext.define('MPAFiltersWindow.filterModel', {
					extend: 'Ext.data.Model',
					fields: [
						'id', 'text', 'filterType', 'selectionType', 'url'
					],
					idProperty: 'id'
				});
		
				this.treeStore = Ext.create('Ext.data.TreeStore', {
					model: this.filterModel,
					proxy: {
						type: 'ajax',
						url: '/static/js/json/filters.js',
						reader: {
							type: 'json'
						}
					}
				});
				this.treeStore.load();
				
				this.treePanel = Ext.create('Ext.tree.Panel', {
					height: 245,
					bodyStyle: 'background-color: #FFFFFF;',
					autoScroll: true,
					rootVisible: false,
					store: this.treeStore
				});
		
				this.treePanel.on('select', function (sm, rec, idx) {
					MPAFiltersWindow.processTreeSelect(sm, rec, idx);
				});		
			},
			
			loadSelectionGrid: function () {
				
				Ext.define('MPAFiltersWindow.gridModel', {
					extend: 'Ext.data.Model',
					fields: [
						'id', 'name'
					],
					idProperty: 'id'
				});
		
				this.gridStore = Ext.create('Ext.data.Store', {
					model: this.gridModel,
					proxy: {
						type: 'ajax',
						reader: {
							type: 'json'
						}
					},
					listeners: {
						load: function (store) {
							store.sort('name', 'ASC');
							MPAFiltersWindow.setGridFilterSelections();
						}
					}
				});
		
				this.gridSelModel = Ext.create("Ext.selection.CheckboxModel", {
					checkOnly: true
				});
		
				this.gridPanel = Ext.create('Ext.grid.Panel', {
					hidden: true,
					height: 255,
					bodyStyle: 'background-color: #FFFFFF;',
					border: false,
					title: 'Select One or More Values',
					selModel: this.gridSelModel,
					sortableColumns: false,
					forceFit: true,
					columns: [
						{
							id: 'name',
							dataIndex: 'name',
							width: 275
						}
					],
					rowLines: false,
					columnLines: false,
					hideHeaders: true,
					viewConfig: {
						trackOver: false,
						stripeRows: false
					},
					store: this.gridStore,
					listeners: {
						selectionChange: function (sm, recs) {
							MPAFiltersWindow.getGridFilterValues(sm);
						}
					}
				});		
			},
			
			loadPanels: function () {
		
				this.instructionPanel = Ext.create('Ext.Panel', {
					//hidden: true,
					height: 255,
					bodyStyle: 'padding: 10px;',
					html: 'First select a Filter category on the left and then you can choose the values used to filter the MPAs.'
				});
				
		
				this.minmaxPanel = Ext.create('Ext.form.Panel', {
					hidden: true,
					height: 255,
					bodyStyle: 'padding:10px;',
					frame: true,
					title: 'Enter Min and/or Max Values',
					defaults: {
						labelAlign: 'right',
						labelWidth: 110
					},
					items: [
						{
							xtype: 'numberfield',
							fieldLabel: 'Minimum',
							width: 180
						},
						{
							xtype: 'numberfield',
							fieldLabel: 'Maximum',
							width: 180
						}
					]
				});
				
				this.selectionPanel = Ext.create('Ext.Panel', {
					height: 255,
					border: false,
					bodyStyle: 'background-color: #FFFFFF;',
					items: [
						this.instructionPanel,
						this.gridPanel,
						this.minmaxPanel
					]
				});
				
			},
			
			processTreeSelect: function (sm, rec, idx) {
				this.filterID = rec.get('id');
				var fltrType = rec.get('filterType');
				var selType = rec.get('selectionType');
				var url = rec.get('url');
				
				this.instructionPanel.hide();
				this.btnAddFilter.disable();
				
				if (selType === 'multigrid') {
					this.minmaxPanel.hide();
					this.gridStore.removeAll();
					this.gridStore.getProxy().url = url;
					this.gridStore.load();
					this.gridPanel.show();
				} else if (selType === 'minmax') {
					this.gridPanel.hide();
					this.minmaxPanel.show();			
				}
			},
			
			setGridFilterSelections: function () {
				var selected = this.filters.get(this.filterID);
				if (!selected) {
					return;
				}
		
				var id = null, rec = null;
				var k = 0, len = selected.getCount();
				for (k = 0; k < len; k++) {
					id = selected.getAt(k).get('id');
					rec = this.gridStore.findRecord('id', id);
					if (rec) {
						this.gridSelModel.select(rec, true, true);
						this.btnAddFilter.enable();
					}
				}
			},
			
			getGridFilterValues: function (sm) {
				var selected = sm.selected.clone();
		
				this.filters.remove(this.filterID);
				if (selected.getCount() > 0) {
					this.filters.add(this.filterID, selected);
					this.btnAddFilter.enable();
				} else {
					this.btnAddFilter.disable();
				}
			},
			
			isFiltered: function () {
				return this.filtered;
			},
			
			addFilter: function () {
				var selected = this.filters.get(this.filterID);
				if (!selected) {
					return;
				}
				var values = [];
				selected.each(function (item) {
					values.push(item.get('id'));	
				});
				
				// quick & dirty. there's a better way to do this
				var val = Ext.JSON.decode('{"' + this.filterID + '": ' + Ext.JSON.encode(values) + '}');
				this.mapFilters.replace(this.filterID, val);
					
				
				// now we're ready to go...
				this.hideWindow();
				this.showMask("Searching MPAs<br/>Please wait...");
				var tsk = new Ext.util.DelayedTask(this.applyMapFilters, this);
				tsk.delay(10);
			},
			
			clearFilters: function () {
						this.map.clusterer.clearMarkers();
				this.filters.clear();
				this.mapFilters.clear();
				this.gridStore.load();
						this.filtered = false;        
						if (MPALayersWindow) {
								MPALayersWindow.loadLayers();
						}		
			},
			
			applyQSFilter: function () {
				var qs = new mpatlas.utils.queryString();
				var filter = qs.get('filter');
				if (filter) {
					var arr = Ext.JSON.decode(filter);
					var k = 0, len = arr.length;
					var fKey, fArr;
		
					for (k = 0; k < len; k++) {
						filter = arr[k];
						for (fKey in filter) {
							fArr = filter[fKey];
							var fk, fLen = fArr.length;
							var id, fRecs = new Ext.util.MixedCollection();
							if (fLen > 0) {
								this.mapFilters.add(fKey, filter);
		
								for (fk = 0; fk < fLen; fk++) {
									id = fArr[fk];
									var item = Ext.create('MPAFiltersWindow.filterModel', {
										id: id
									});
									fRecs.add(fk, item);
								}
								this.filters.add(fKey, fRecs);
							}
						}
					}
					
					if (this.mapFilters.getCount() > 0) {
						this.applyMapFilters();
					}
				}		
			},
			
			applyMapFilters: function () {
				// get all filters as an array
				var arr = this.mapFilters.getRange();
				var str = Ext.JSON.encode(arr);
		
				this.map.clusterer.clearMarkers();
		
				// set the url
				var url = mpatlas.domain + 'mpa/sites/ids/?filter=' + str;
				if (mpatlas.proxy && mpatlas.proxy !== '') {
					url = mpatlas.proxy + escape(url);
				}
				Ext.Ajax.request({
					url: url,
					timeout: 120000,
					success: this.addMarkers,
					scope: this
				});
			},
		
			addMarkers: function (resp) {
				var pts = [];
				this.markers = [];
		
				this.updateMask("Applying Filters<br/>Please wait...");
				var json = this.getJSONFromResponse(resp);
				if (json) {
					var mpas = json.mpas; 
					var k = 0, len = mpas.length;
					var id = null, point = null, geom = null, coords = null, marker = null;
		
			
					for (k = 0; k < len; k++) {
						id = mpas[k];
						point = this.points.get(id);
						if (point) {
							geom = point.geometry;
							if (geom) {					
								coords = geom.coordinates;
								lat = coords[1];
								lng = coords[0];						
								pos = new L.LatLng(lat, lng);
								
								// for the bounding box
								pts.push(pos);
		
								marker = new L.Marker(pos);
								this.markers.push(marker);
			
								// extra marker to the right
								pos = new L.LatLng(lat, lng + 360, true);
								marker = new L.Marker(pos);
								this.markers.push(marker);
			
								// extra marker to the left
								pos = new L.LatLng(lat, lng - 360, true);
								marker = new L.Marker(pos);
								this.markers.push(marker);
							}
						}
					}
					
					if (pts.length > 0) {
						this.bounds = new L.LatLngBounds(pts);	
						this.map.map.fitBounds(this.bounds);
						
						if (this.markers.length > 0) {
							this.map.clusterer.addMarkers(this.markers);
						}
						
						this.filtered = true;
					} else {
						Ext.MessageBox.alert('No results', 'There are no MPAs that<br/>match your selected filter.');
					}
			
					if (MPALayersWindow) {
						MPALayersWindow.loadLayers();
					}
					
				}
		
						this.hideMask();
		
				},
				
			showMask: function (msg) {
				this.mask = new Ext.LoadMask('leafletmap', {msg: msg});
				this.mask.show();		
			},
		
			updateMask: function (msg) {
				if (this.mask) {
					this.mask.update(msg);
				}
			},
			
			hideMask: function () {
				if (this.mask) {
					this.mask.hide();
					this.mask.destroy();
				}
			},
		
			showWindow: function () {
				this.window.show();
				this.window.alignTo('leafletmap', 'c-c');
			},
			
			hideWindow: function () {
				this.window.hide();
			},
			
			getJSONFromResponse: function (response) {
				var s = null, json = null;
				try {
					json = response.responseJSON;
					if (!json) {
						s = response.responseText;
						if ((s !== undefined) && (s !== '')) {
							json = Ext.decode(s);
						} else if (response.transport) {
							s = response.transport.responseText;
							if ((s !== undefined) && (s !== '')) {
								json = Ext.decode(s);
							}
						}
					}
				} catch (e) {}
				return json;
			}	
		};
	}
)