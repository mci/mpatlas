define(
	[
		//** TODO had to drop back to 4.0.7 because of IE compatability issues. Still not perfect. Revisit later
		//'http://cdn.sencha.io/ext-4.0.7-gpl/ext-all.js'
		//'//cdn.terraweave.com/v/6.0/extjs/ext-all.js'
		'extjs'
	],
	function () {

		Ext.define('MPAList', {
			singleton: true,
			
			constructor: function (options) {
				this.SearchTask = Ext.create('Ext.util.DelayedTask', this.filterStore, this);
				this.callParent();
			},
			
			//** TODO be sure to set the proxy and domain before sending to production!
			proxy: '',
			domain: 'http://' + document.domain + '/',
			/*
			proxy: '/terraweave/features.ashx?url=', // needed for testing cross-domain
			domain: 'http://mpatlas.org/',
			*/

			filterMinChars: 3,
		
			filterStore: function () {
				var val = this.TextSearch.getValue();
				if (val || val.length >= this.filterMinChars) {
					var st = this.Store;
					if (st.filters && st.filters.getCount() > 0) {
						st.filters.clear();
					}
					st.filter('name', val);
					this.ButtonClearFilter.enable();
				}
			},
		
			clearFilter: function (clearVal) {
				this.SearchTask.cancel();
				this.Store.filters.clear();
				this.Store.load();
				if (clearVal !== false) {
					this.TextSearch.setValue('');
				}
				this.ButtonClearFilter.disable();     
			},
			

			ButtonClearFilter: Ext.create('Ext.Button', {
				text: 'Clear Filter',
				disabled: true,
				handler: function () {
					MPAList.clearFilter();
				}
			}),
			
			TextSearch: Ext.create('Ext.form.TextField', { 
				width: 150,
				listeners: {
					'change': function (field, newVal, oldVal, options) {
						var m = MPAList;
						if (newVal.length >= m.filterMinChars) {
							m.SearchTask.delay(250);
						} else {
							if (m.Store.filters.getCount() > 0) {
								m.clearFilter(false);
							}
						}
					}
				}
			})
		});
		
		Ext.define('MPAList.Model', {
			extend: 'Ext.data.Model',
			fields: [
				'id', 'name', 'designation', 'country', 'url', 'point_within', 'bbox_ll', 'bbox_ur'
			],
			idProperty: 'id'
		});
		
		// create the Data Store
		Ext.define('MPAList.Store', {
			extend: 'Ext.data.Store',
			model: 'MPAList.Model',
			singleton: true,
		
			constructor : function (options) {
				this.callParent();
				this.on('beforeLoad', this.setProxyURL, this);
			},
			
			remoteSort: true,
			remoteFilter: true,
			pageSize: 75,
			
			proxy: {
				type: 'ajax',
				url: this.proxy,
				
				// we override the url. this. cleans up the additional params
				limitParam: null,
				startParam: null,
				pageParam: null,
				sortParam: null,
				filterParam: null,
				noCache: false, // we want these requests to be cached in browser and server memcached
				
				reader: {
					type: 'json',
					root: 'mpas',
					totalProperty: 'total_count'
				},
				
				// sends single sort as multi parameter
				simpleSortMode: false
			},
		
			sorters: [
				{
					property: 'name',
					direction: 'ASC'
				}
			],
			
			setProxyURL: function (store, operation, options) {
				if (!operation) {
					return;
				}
		
				var pr = store.getProxy();
				var m = MPAList;
				var remoteURL =  m.domain + 'mpa/sites/json/';
				
				// add the filter(s)
				remoteURL += '?q=';
				if (operation.filters && operation.filters.length > 0) {
					
					// get just the first one  (assuming one for now)
					var filter = operation.filters[0];
					remoteURL += filter.value;
				}
		
				// add the sorter(s)
				if (operation.sorters && operation.sorters.length > 0) {
					var sort = operation.sorters[0];
					
					if (sort.property === 'designation') {
						sort.property = 'designation_eng';
					}
					remoteURL += '&sort=' + sort.property;
					if (sort.direction) {
						remoteURL += '&dir=' + sort.direction.toLowerCase();
					} else {
						remoteURL += '&sort=asc';
					}
				}
				
				// add the paging parameters
				if (operation.limit) {
					remoteURL += '&paginate_by=' + operation.limit;
					remoteURL += '&page=' + ((operation.start / operation.limit) + 1);
				} else {
					remoteURL += '&paginate_by=1';
					remoteURL += '&page=0';
				}
		
				// set the url
				if (m.proxy && m.proxy !== '') {
					pr.url = m.proxy + escape(remoteURL);
				} else {
					pr.url = remoteURL;
				}
			}
		});
		
		Ext.define('MPAList.Grid', {
			extend   : 'Ext.grid.Panel',
			
			constructor : function (options) {
				this.columns = this.buildColumns();
				
				this.store = MPAList.Store;
				this.store.on('beforeLoad', this.beforeLoad, this);
				this.store.on('load', this.afterLoad, this);
				
				this.callParent();
		
				this.getFilter();
				//this.getSorters();
				this.store.load();
				Ext.EventManager.onWindowResize(this.resizeGrid, this);

			},
			
			width: 500,
			height: 200,
			loadMask: true,
			multiSelect: false,
			columnLines: true,
			stripeRows: true,
			viewConfig: {
				trackOver: false
			},
			
			disableSelection: true,
		
			dockedItems: [{
				xtype: 'pagingtoolbar',
				store: MPAList.Store,   // same store GridPanel is using
				dock: 'bottom',
				displayInfo: true
			}],
		
			tbar: [
				"&nbsp;&nbsp;<b>Search the MPAs:&nbsp;</b>",
				MPAList.TextSearch,
				"&nbsp;Enter at least " + MPAList.filterMinChars + " letters to filter the list",
				"->",
				MPAList.ButtonClearFilter
			],
		
			renderTo: 'mpa-list-container',
			
			buildColumns : function () {
		
				function renderName(value, p, record) {
					return Ext.String.format(
						'<a href="' + MPAList.domain + 'mpa/sites/{1}/">{0}</a>',
						value,
						record.get('id')
					);
				}
		
				function renderIcon(value, p, record) {
					var pt = record.get('point_within');
					var bbox_ll = record.get('bbox_ll');
					var bbox_ur = record.get('bbox_ur');
					if (!pt || !bbox_ll || !bbox_ur) {
						return "";
					} else {
						return Ext.String.format(
							'<a href="javascript:void(0);" onclick="mpatlas.zoomToMPA({id:{0},pt:[{1}],bbox:[{2},{3}]})"><img src="http://static.mpatlas.org/images/header_searchbutton.png" style="height:16px;width:16px;" /></a>',
							value,
							pt.coordinates,
							bbox_ll.coordinates,
							bbox_ur.coordinates
						);							
					}
				}
	
				return [
					{
						xtype: 'rownumberer',
						width: 40,
						sortable: false,
						menuDisabled: true
					},
					{
						tdCls: 'x-grid-cell-topic',
						text: "MPA",
						dataIndex: 'name',
						flex: 1,
						renderer: renderName,
						sortable: true,
						menuDisabled: true
					},
					{
						text: "Designation",
						dataIndex: 'designation',
						width: 270,
						sortable: true,
						menuDisabled: true
					},
					{
						text: "Country",
						dataIndex: 'country',
						width: 120,
						sortable: true,
						menuDisabled: true
					},
					{
						text: "&nbsp;",
						dataIndex: 'id',
						width: 30,
						renderer: renderIcon,
						sortable: false,
						menuDisabled: true
					}
				];
			
			},
		
			getFilter: function () {
				var filters = null, filter = null;
				try {
					filters = mpatlas.history.get('MPAFilters', true);
				} catch (e) {}
				
				if (filters && filters.length > 0) {
					this.store.filters.addAll(filters);
					
					var len = filters.length;
					var val = null;
					var k = 0;
					for (k = 0; k < len; k++) {
						filter = filters[k];
						if (filter.property === 'name') {
							val = filter.value;
							break;
						}
					}
					if (val) {
						MPAList.TextSearch.setRawValue(val);
						MPAList.ButtonClearFilter.enable();
					}
				}
			},
			
			getSorters: function () {
				var sort = null, sorters = null;
				try {
					sorters = mpatlas.history.get('MPASorters', true);
				} catch (e) {}

				if (!sorters) {
					sorters = [
						{
							property: 'name',
							direction: 'ASC'
						}
					];
				}				
				if (sorters && sorters.length > 0) {
					this.store.sorters.addAll(sorters);					
				}
			},

			beforeLoad: function (store, operation, options) {
				if (operation.filters && operation.filters.length > 0) {
					try {
						mpatlas.history.set('MPAFilters', operation.filters, true);
					} catch (e) {}
				}
				if (operation.sorters && operation.sorters.length > 0) {
					try {
						mpatlas.history.set('MPASorters', operation.sorters, true);
					} catch (e2) {}
				}

				var el = Ext.fly('stats_mpas_current_filter');
				if (el) {
					el.update('Updating...');
				}
			},
			
			afterLoad: function (store) {
				var cnt = store.getTotalCount();
				var el = Ext.fly('stats_mpas_current_filter');
				if (el) {
					if (cnt === 9042) { //** TODO I know this should not be hard coded
						el.update('Showing all MPAs');
					} else {
						el.update(Ext.String.format("Showing {0} MPAs<br />based on current filter", Ext.util.Format.number(cnt, ',')));				
					}
				}
			},
			
			resizeGrid: function () {
				if (!this.isVisible()) {
					return;
				}
				var bg = Ext.fly('list-bg');
				var sz = bg.getSize();
				var container = Ext.fly('mpa-list-container');		
				sz.height -= container.getTop(true);				
				this.setSize(sz);
				this.doLayout();
				
				// work around for funky scroller sizing in Chrome
				if (Ext.isChrome) {
					var scr = $('#mpa-list-container .x-scroller-ct');
					scr.css('width', 'auto');
					var str = $('#mpa-list-container .x-stretcher');
					str.css('width', 'auto');
				}
			}			
		});
		
		/*
		Ext.Loader.setConfig({enabled: true});
		Ext.require([
			'Ext.grid.*',
			'Ext.data.*'
		]);
		*/

		// Ext.onReady not firing for IE due to an undetermined conflict with another lib (why do we needs so many libs!)
		// so we do it the JQuery way. This screws up the layout
		//if (Ext.isIE9) {
		//	$(document).ready(function () {
		//		MPAList.List = Ext.create('MPAList.Grid');
		//	});
		//} else {
		Ext.Loader.onReady(function () {
			MPAList.List = Ext.create('MPAList.Grid');
			try {
				var qs = new mpatlas.utils.queryString();
				var list = qs.get('list');
				if (list) {
					mpatlas.switchToListView();
				}
			} catch (e) {}
		}, this, true);
		//}
	}
);