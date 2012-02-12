define([
	'//cdn.terraweave.com/v/6.0/extjs/ext-all.js'
],
function () {
	Ext.define('MPAtlas.list', {
		singleton: true,
		
		constructor: function (options) {
			this.SearchTask = Ext.create('Ext.util.DelayedTask', this.filterStore, this);
			this.callParent();
		},
		
		//proxy: '/terraweave/features.ashx?url=', // needed for testing cross-domain
		url: 'http://mpatlas.org/mpa/sites/json/',
		filterMinChars: 2,
	
		filterStore: function () {
			var val = this.TextSearch.getValue();
			if (val || val.length > this.filterMinChars) {
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
				this.TextSearch.setValue();
			}
			this.ButtonClearFilter.disable();     
		},
		
		ButtonClearFilter: Ext.create('Ext.Button', {
			text: 'Clear Filter',
			disabled: true,
			handler: this.clearFilter,
			scope: this
		}),
		
		TextSearch: Ext.create('Ext.form.TextField', { 
			width: 150,
			//emptyText: 'Search MPAs',
			listeners: {
				'change': function (field, newVal, oldVal, options) {
					var m = MPAtlas.list;
					if (newVal.length > m.filterMinChars) {
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
	
	Ext.define('MPAtlas.list.Model', {
		extend: 'Ext.data.Model',
		fields: [
			'id', 'name', 'designation', 'country', 'url'
		],
		idProperty: 'id'
	});
	
	// create the Data Store
	Ext.define('MPAtlas.list.Store', {
		extend: 'Ext.data.Store',
		requires: ['MPAtlas.list.Model'],
		model: 'MPAtlas.list.Model',
		singleton: true,
	
		constructor : function(options) {
			this.callParent();
			this.on('beforeLoad', this.setProxyURL, this);
		},
		
		remoteSort: true,
		remoteFilter: true,
		pageSize: 250,
		
		proxy: {
			type: 'ajax',
			url: this.proxy,
			
			// we override the url. this. cleans up the additional params
			limitParam: null,
			startParam: null,
			pageParam: null,
			sortParam: null,
			filterParam: null,
			
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
		
		setProxyURL: function(store, operation, options) {
			if (!operation) {
				return;
			}
	
			var pr = store.getProxy();
			var m = MPAtlas.list;
			var remoteURL =  m.url;
			
			// add the filter(s)
			remoteURL += '?q=';
			if (operation.filters && operation.filters.length > 0) {
				
				// get just the first one  (assuming one for now)
				var filter = operation.filters[0];
				remoteURL += filter.value;
			}
	
			// add the sorter
			if (operation.sorters && operation.sorters.length > 0) {
				var sort = operation.sorters[0];
				if (sort.property === 'designation') {
					sort.property = 'desig_eng';
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
	
	Ext.define('MPAtlas.list.Grid', {
		extend   : 'Ext.grid.Panel',
		requires : ['MPAtlas.list.Store'],
		
		constructor : function (options) {
			this.mpatlas = options.mpatlas;
			this.columns = this.buildColumns();
			
			this.store   = MPAtlas.list.Store;
			this.store.on('beforeLoad', this.saveFilter, this);
			
			this.callParent();
	
			this.getFilter();
			this.store.load();        
		},
		
		width: 500,
		height: 200,
		loadMask: true,
		multiSelect: false,
		columnLines: true,
		stripeRows: true,
		selModel: {
		  pruneRemoved: false
		},
		viewConfig: {
			trackOver: false
		},
		
		// Use a PagingGridScroller (this is interchangeable with a PagingToolbar)
		verticalScrollerType: 'paginggridscroller',
		
		// do not reset the scrollbar when the view refresh
		invalidateScrollerOnRefresh: true,
		// infinite scrolling does not support selection
		disableSelection: true,
	
		dockedItems: [{
			xtype: 'pagingtoolbar',
			store: MPAtlas.list.Store,   // same store GridPanel is using
			dock: 'bottom',
			displayInfo: true
		}],
	
		tbar: [
			"&nbsp;&nbsp;<b>Search the MPAs:&nbsp;</b>",
			MPAtlas.list.TextSearch,
			"&nbsp;Enter at least " + MPAtlas.list.filterMinChars + " letters to filter the list",
			"->",
			MPAtlas.list.ButtonClearFilter
		],
	
		renderTo: 'mpa-list-container',
		
		 buildColumns : function() {
	
			function renderName(value, p, record) {
				return Ext.String.format(
					'<a href="http://mpatlas.org{1}">{0}</a>',
					value,
					record.get('url')
				);
			}
	
			function renderIcon(value, p, record) {
				return Ext.String.format(
					'<a href="#" onclick="mpatlas.zoomTomMPA({1})"><img src="http://static.mpatlas.org/images/header_searchbutton.png" style="height:16px;width:16px;" /></a>',
					value
				);
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
			var filters = this.mpatlas.history.get('MPAFilters', true);
			if (filters && filters.length > 0) {
				//apply filter here
				this.store.filters.addAll(filters);
				
				var len = filters.length;
				var val = null;
				for (var k = 0; k < len; k++) {
					filter = filters[k];
					if (filter.property === 'name') {
						val = filter.value;
						break;
					}
				}
				if (val) {
					MPAtlas.list.TextSearch.setValue(val);
				}				
			}
		},
		
		saveFilter: function (store, operation, options) {
			if (operation.filters && operation.filters.length > 0) {
				this.mpatlas.history.set('MPAFilters', operation.filters, true);
			}
		}
	});
	
	Ext.Loader.setConfig({enabled: true});
	Ext.require([
		'Ext.grid.*',
		'Ext.data.*'
	]);
});