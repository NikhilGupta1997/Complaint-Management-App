# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
	"""
	example action using the internationalization operator T and flash
	rendered by views/default/index.html or views/generic.html

	if you need a simple wiki simply replace the two lines below with:
	return auth.wiki()
	"""
	if (auth.user):
		response.flash = T("Welcome " + auth.user.name + " to Complaint Management System")
	else:
		response.flash =T("Welcome to Complaint Management System")
	return dict(noti_count=4)

def notifications():
	# return dict(notifcations=auth.user.username)
	noti = db(db.notifications.dest_user_id==auth.user.username).select(orderby=~db.notifications.time_stamp)
	db(db.notifications.dest_user_id==auth.user.username).update(seen=1)
	return dict(notifications=noti)

def get_hostel():
	if ("hostel_id" in request.vars):
		category_id = int(request.vars.hostel_id)
		pref=None
		if category_id>=0:
			pref =  db(db.hostel_mapping.hostel_id==category_id).select()
		else:
			pref = db(db.hostel_mapping.hostel_id>=0).select()
		return dict(Hostel=pref)
	else:
		return dict(Hostel = False)

def logged_in():
	return dict(success=auth.is_logged_in(), user=auth.user)

def logout():
	if (auth.user):
		return dict(success=True, loggedout=auth.logout())
	else:
		return dict(success="did not work")

@auth.requires_login()
def settings():
	return dict(success= True)

@auth.requires_login()
def change_pwd():
	return dict(success=True)

@auth.requires_login()
def newcomplaint():    
	try:
		tab=str(request.args[0])
	except:
		tab="indiv"
	categories=db(db.complaint_category.category_id>=0).select()
	return dict(success=True,tab=tab,categories=categories)

def newcompl():
	t1 = request.args[0]
	complaint_content=request.vars.complaint_content
	extradet=request.vars.extra_info
	comptype=int(request.vars.complaint_type)
	anon=int(request.vars.anonymous)
	usname=auth.user.username
	if t1=="indiv":
		hostelid = GetHostelID(auth.user.username)
		# and (db.admin_info.hostel_id<0 or db.admin_info.hostel_id==GetHostel(auth.user.username()))
		people = db((db.admin_info.complaint_area==comptype) & (db.admin_info.hostel_id==hostelid)).select(orderby=~db.admin_info.admin_level)
		if len(people)==0:
			people = db((db.admin_info.complaint_area==comptype) & (db.admin_info.hostel_id<0)).select(orderby=~db.admin_info.admin_level)
		if len(people)==0:
			return dict(success=False,complaint_content="no admin found")
		people=people[0]
		peopleid = people["username"]
		NewCompId=GetNewCompId(0)
		db.indiv_complaints.insert(
			complaint_id=NewCompId,
			username=usname,
			complaint_type=comptype,
			complaint_content=complaint_content,
			extra_info=extradet,
			admin_id=peopleid)
		db.complaint_user_mapping.insert(complaint_id=NewCompId,user_id=usname)
		db.complaint_user_mapping.insert(complaint_id=NewCompId,user_id=peopleid)
		db.notifications.insert(complaint_id=NewCompId,src_user_id=usname,dest_user_id=peopleid,description="New complaint!")        
		return dict(success=True,complaint_content=complaint_content,extra_info=extradet)
	elif t1=="hostel":
		hostelid = GetHostelID(auth.user.username)
		# and (db.admin_info.hostel_id<0 or db.admin_info.hostel_id==GetHostel(auth.user.username()))
		people = db((db.admin_info.complaint_area==comptype) & (db.admin_info.hostel_id==hostelid)).select(orderby=~db.admin_info.admin_level)
		if len(people)==0:
			people = db((db.admin_info.complaint_area==comptype) & (db.admin_info.hostel_id<0)).select(orderby=~db.admin_info.admin_level)
		if len(people)==0:
			return dict(success=False,complaint_content="no admin found")
		people=people[0]
		peopleid = people["username"]
		NewCompId=GetNewCompId(1)
		db.hostel_complaints.insert(
			complaint_id=NewCompId,
			username=usname,
			hostel=hostelid,
			complaint_type=comptype,
			complaint_content=complaint_content,
			extra_info=extradet,
			admin_id=peopleid,
			anonymous=anon
			)
		db.complaint_user_mapping.insert(complaint_id=NewCompId,user_id=usname)
		db.complaint_user_mapping.insert(complaint_id=NewCompId,user_id=peopleid)
		db.notifications.insert(complaint_id=NewCompId,src_user_id=usname,dest_user_id=peopleid,description="New complaint!")        
		return dict(success=True,complaint_content=complaint_content,extra_info=extradet)
	elif t1=="insti":
		hostelid = GetHostelID(auth.user.username)
		# and (db.admin_info.hostel_id<0 or db.admin_info.hostel_id==GetHostel(auth.user.username()))
		people = db((db.admin_info.complaint_area==comptype) & (db.admin_info.hostel_id<0)).select(orderby=~db.admin_info.admin_level)
		if len(people)==0:
			return dict(success=False,complaint_content="no admin found")
		people=people[0]
		peopleid = people["username"]
		NewCompId=GetNewCompId(2)
		db.insti_complaints.insert(
			complaint_id=NewCompId,
			username=usname,
			hostel=hostelid,
			complaint_type=comptype,
			complaint_content=complaint_content,
			extra_info=extradet,
			admin_id=peopleid,
			anonymous=anon
			)
		db.complaint_user_mapping.insert(complaint_id=NewCompId,user_id=usname)
		db.complaint_user_mapping.insert(complaint_id=NewCompId,user_id=peopleid)
		db.notifications.insert(complaint_id=NewCompId,src_user_id=usname,dest_user_id=peopleid,description="New complaint!")        
		return dict(success=True,complaint_content=complaint_content,extra_info=extradet)
		
	return dict(success=False,complaint_content=request.args[0],extra_info=extradet)

@auth.requires_login()
def AllComplaints():
	tab="indiv"
	# if len(request_args)<1:
	try:
		tab=str(request.args[0])
	except:
		tab="indiv"
	return dict(success=True,tab=tab)

@auth.requires_login()
def addusers():
	return dict(success=True)

@auth.requires_login()
def complaint():
	complaint =None
	comptype=-1
	admin=0
	dummy="valid"
	comments=[]
	admindetails=None
	complainant=None
	try:
		tab=str(request.args[0])
		if tab[:2]=="i_":
			comps = db(db.indiv_complaints.complaint_id==tab).select()
			if len(comps):
				complaint=comps[0]
				comptype=0
		elif tab[:2]=="h_":
			comps = db(db.hostel_complaints.complaint_id==tab).select()
			if len(comps):
				complaint=comps[0]
				comptype=1
		elif tab[:2]=="in":
			comps = db(db.insti_complaints.complaint_id==tab).select()
			if len(comps):
				complaint=comps[0]
				comptype=2
		if complaint:
			admin=(auth.user.username==complaint["admin_id"])
			admindetails = db(db.users.username==complaint["admin_id"]).select()[0]
			complainant=db(db.users.username==complaint["username"]).select()[0]
		comments=db(db.comments_complaint.complaint_id==tab).select()
	except:
		y=5
		dummy="invalid"
	try:
		comment = request.vars.comment
		if comment:
			db.comments_complaint.insert(
				complaint_id = complaint["complaint_id"],
				user_id = auth.user.username,
				description=comment
			)
		comments=db(db.comments_complaint.complaint_id==tab).select()        
	except:
		comment=""    
	return dict(complaint=complaint,complainant=complainant,comptype=comptype,admindetails=admindetails,admin=admin,comments=comments,dummy=dummy)

def managecomplaints():    
	tab="indiv"
	# if len(request_args)<1:
	try:
		tab=str(request.args[0])
	except:
		tab="indiv"
	return dict(success=True,tab=tab)

def user():
	"""
	exposes:
	http://..../[app]/default/user/login
	http://..../[app]/default/user/logout
	http://..../[app]/default/user/register
	http://..../[app]/default/user/profile
	http://..../[app]/default/user/retrieve_password
	http://..../[app]/default/user/change_password
	http://..../[app]/default/user/manage_users (requires membership in
	use @auth.requires_login()
		@auth.requires_membership('group name')
		@auth.requires_permission('read','table name',record_id)
	to decorate functions that need access control
	"""
	return dict(form=auth())


@cache.action()
def download():
	"""
	allows downloading of uploaded files
	http://..../[app]/default/download/[filename]
	"""
	return response.download(request, db)


def call():
	"""
	exposes services. for example:
	http://..../[app]/default/call/jsonrpc
	decorate with @services.jsonrpc the functions to expose
	supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
	"""
	return service()


@request.restful()
def api():
	response.view = 'generic.'+request.extension
	def GET(*args,**vars):
		patterns = 'auto'
		parser = db.parse_as_rest(patterns,args,vars)
		if parser.status == 200:
			return dict(content=parser.response)
		else:
			raise HTTP(parser.status,parser.error)
	def POST(table_name,**vars):
		if not(table_name=="login_post"):
			raise HTTP(400)
		else:
			userid = request.vars.userid
			password = request.vars.password
			user = auth.login_bare(userid,password)
			admin = db(db.admin_info.username==userid).select()
			special = db((db.users.username==userid)&(db.users.user_type<0)).select()
			return dict(success=False if not user else True, special=(len(special)>0),admin=(len(admin)>0),Unique_Id=user["username"] if user else "",userid =userid,passwd =password)
			# return dict(variables=list(vars),var2=request.vars)
		return db[table_name].validate_and_insert(**vars)
	def PUT(table_name,record_id,**vars):
		return db(db[table_name]._id==record_id).update(**vars)
	def DELETE(table_name,record_id):
		return db(db[table_name]._id==record_id).delete()
	return dict(GET=GET, POST=POST, PUT=PUT, DELETE=DELETE)

def login():
	userid = request.vars.userid
	password = request.vars.password
	user = auth.login_bare(userid,password)
	admin = db(db.admin_info.username==userid).select()
	special = db((db.users.username==userid)&(db.users.user_type<0)).select()
	return dict(success=False if not user else True, special=(len(special)>0),admin=(len(admin)>0),Unique_Id=user["username"] if user else "",userid =userid,passwd =password)

def change_pass():
	# oldpassword = request.vars.oldpwd
	newpassword = request.vars.newpwd
	table_user=auth.settings.table_user
	passfield = auth.settings.password_field
	s=db(table_user.id== auth.user_id)
	d={passfield: newpassword}
	temp = s.validate_and_update(**d)
	response.flash = T("Password Changed Successfully")
	return dict(success= temp,newpwd=newpassword)

# @auth.requires_login
def change_passwd1():
	# return dict(success=True)
	# oldpassword = request.vars.oldpwd
	newpassword = request.vars.newpwd
	table_user=auth.settings.table_user
	passfield = auth.settings.password_field
	s=db(table_user.id== auth.user_id)
	d={passfield: newpassword}
	temp = s.validate_and_update(**d)
	# response.flash = T("Password Changed Successfully")
	return dict(success= temp,newpwd=newpassword)


def clear_db():
	for table in db.tables():
		try:
			db(db[table].id>0).delete()
			print "Cleared",table
		except Exception, e:
			print "Couldn't clear",table

def add_user():
	if (auth.is_logged_in()):
		usertype = int(db(db.users.username == auth.user.username).select()[0]["user_type"])
		bool_admin=False
		if usertype<0:
			name=request.vars.name
			user_type=int(request.vars.user_type)
			username=request.vars.username
			contact_number=request.vars.contact_number
			hostel=request.vars.hostel
			password=request.vars.password
			bool_admin=True
			db.users.insert(name=name,user_type=user_type,username=username,contact_number=contact_number,hostel=hostel,password=password)
			return dict(success=bool_admin,Name=name, Unique_Id=username,userid =user_type,contact_number=contact_number,hostel=hostel,passwd =password)		
		else:
			return dict(success = False)

def add_admin():
	if (auth.is_logged_in()):
		usertype = int(db(db.users.username == auth.user.username).select()[0]["user_type"])
		bool_admin=False
		if usertype<0:
			username = request.vars.username
			c_area=int(request.vars.category)
			hostel=int(request.vars.hostel)
			desc=request.vars.desc
			level=int(request.vars.level)
			bool_admin=True
			users = db(db.users.username == username).select()
			if len(users)>0:
				db.admin_info.insert(username=username,hostel_id=hostel,complaint_area = c_area,admin_level=level,description=desc)
				return dict(success=bool_admin,Name=name, Unique_Id=username,userid =user_type,contact_number=contact_number,hostel=hostel,passwd =password)
	return dict(success = False)

def populate_db():
	## Populate DB Script

	## clear database
	for table in db.tables():
		try:
			db(db[table].id>0).delete()
			print "Cleared",table
		except Exception, e:
			print "Couldn't clear",table

	## create 4 students
	db.users.insert(
		name="Aditi",
		user_type=-1,
		username="cs1140205",
		contact_number="9876543210",
		hostel=1,
		password="aditi",
	)

	db.users.insert(
		name="Aayan",
		user_type=0,
		username="cs1140201",
		contact_number="9876543210",
		hostel=2,
		password="aayan",
	)

	db.users.insert(
		name="Bhagee",
		user_type=0,
		username="cs5140297",
		contact_number="9876543210",
		hostel=3,
		password="bhagee",
	)
	
	db.users.insert(
		name="Ayush",
		user_type=0,
		username="cs1140091",
		contact_number="blah blah",
		hostel=1,
		password="ayush",
	)

	db.users.insert(
		name="Nikhil",
		user_type=0,
		username="cs5140462",
		contact_number="blah blah blah",
		hostel=3,
		password="nikhil",
	)

	db.users.insert(
		name="Electrician 1",
		user_type=0,
		username="a001",
		contact_number="1234567899",
		hostel=-1,
		password="a001")
	db.users.insert(
		name="Electrician 11",
		user_type=0,
		username="a0011",
		contact_number="1234567899",
		hostel=-1,
		password="a0011")
	db.users.insert(
		name="Electrician 12",
		user_type=0,
		username="a0012",
		contact_number="1234567899",
		hostel=-1,
		password="a0012")
	db.users.insert(
		name="Electrician 13",
		user_type=0,
		username="a0013",
		contact_number="1234567899",
		hostel=-1,
		password="a0013")


	db.users.insert(
		name ="Head Electrician",
		user_type=0,
		username="a002",
		contact_number="1234432112",
		hostel=-1,
		password="a002"
	)

	db.users.insert(
		name ="Plumber 1",
		user_type=0,
		username="a003",
		contact_number="9988776655",
		hostel=-1,
		password="a003"
	)
	db.users.insert(
		name ="Plumber 12",
		user_type=0,
		username="a0031",
		contact_number="9988776655",
		hostel=-1,
		password="a0031"
	)
	db.users.insert(
		name ="Plumber 13",
		user_type=0,
		username="a0032",
		contact_number="9988776655",
		hostel=-1,
		password="a0032"
	)
	db.users.insert(
		name ="Plumber 14",
		user_type=0,
		username="a0033",
		contact_number="9988776655",
		hostel=-1,
		password="a0033"
	)
	
	db.users.insert(
		name ="Head Plumber",
		user_type=0,
		username="a004",
		contact_number="9988776655",
		hostel=-1,
		password="a004"
	)


	db.admin_info.insert(
		username="a001",
		complaint_area=1,
		admin_level=2,
		description='Electrician for all hostels',
		hostel_id=0,
	)

	db.admin_info.insert(
		username="a0011",
		complaint_area=1,
		admin_level=2,
		description='Electrician for all hostels',
		hostel_id=1,
	)
	db.admin_info.insert(
		username="a0012",
		complaint_area=1,
		admin_level=2,
		description='Electrician for all hostels',
		hostel_id=2,
	)
	db.admin_info.insert(
		username="a0013",
		complaint_area=1,
		admin_level=2,
		description='Electrician for all hostels',
		hostel_id=3,
	)
	
	
	db.admin_info.insert(
		username="a002",
		complaint_area=1,
		admin_level=1,
		description='Head Electrician for all hostels',
		hostel_id=0,
	)

	# db.admin_info.insert(
	# 	username="a002",
	# 	complaint_area=1,
	# 	admin_level=1,
	# 	description='Head Electrician for all hostels',
	# 	hostel_id=1,
	# )

	# db.admin_info.insert(
	# 	username="a002",
	# 	complaint_area=1,
	# 	admin_level=1,
	# 	description='Head Electrician for all hostels',
	# 	hostel_id=2,
	# )

	# db.admin_info.insert(
	# 	username="a002",
	# 	complaint_area=1,
	# 	admin_level=1,
	# 	description='Head Electrician for all hostels',
	# 	hostel_id=3,
	# )
	
	db.admin_info.insert(
		username="a003",
		complaint_area=2,
		admin_level=2,
		description='Plumber for all hostels',
		hostel_id=0,
	)
	db.admin_info.insert(
		username="a0031",
		complaint_area=2,
		admin_level=2,
		description='Plumber for all hostels',
		hostel_id=1,
	)
	db.admin_info.insert(
		username="a0032",
		complaint_area=2,
		admin_level=2,
		description='Plumber for all hostels',
		hostel_id=2,
	)
	db.admin_info.insert(
		username="a0033",
		complaint_area=2,
		admin_level=2,
		description='Plumber for all hostels',
		hostel_id=3,
	)
	
	
	db.admin_info.insert(
		username="a004",
		complaint_area=2,
		admin_level=1,
		description='Head Plumber for all hostels',
		hostel_id=0,
	)
	# db.admin_info.insert(
	# 	username="a004",
	# 	complaint_area=2,
	# 	admin_level=1,
	# 	description='Head Plumber for all hostels',
	# 	hostel_id=1,
	# )
	# db.admin_info.insert(
	# 	username="a004",
	# 	complaint_area=2,
	# 	admin_level=1,
	# 	description='Head Plumber for all hostels',
	# 	hostel_id=2,
	# )
	# db.admin_info.insert(
	# 	username="a004",
	# 	complaint_area=2,
	# 	admin_level=1,
	# 	description='Head Plumber for all hostels',
	# 	hostel_id=3,
	# )
	
	db.admin_info.insert(
		username="cs1140205",
		complaint_area=6,
		admin_level=2,
		description="BSW Rep for all hostels",
		hostel_id=-1,
	)

	db.admin_info.insert(
		username="cs1140201",
		complaint_area=6,
		admin_level=1,
		description="BSW GSec for all hostels",
		hostel_id=-1,
	)

	db.complaint_category.insert(
		category_id=0,
		category_description="Sports"
	)
	
	db.complaint_category.insert(
		category_id=1,
		category_description="Electricity"
	)
	
	db.complaint_category.insert(
		category_id=2,
		category_description="Water"
	)

	db.complaint_category.insert(
		category_id=3,
		category_description="MessFood"
	)

	db.complaint_category.insert(
		category_id=5,
		category_description="Laundry"
	)

	db.complaint_category.insert(
		category_id=6,
		category_description="BSW_Related"
	)

	db.complaint_category.insert(
		category_id=7,
		category_description="Dance"
	)
	
	db.complaint_category.insert(
		category_id=8,
		category_description="Music"
	)
	
	db.complaint_category.insert(
		category_id=9,
		category_description="Debating"
	)

	db.hostel_mapping.insert(
		hostel_id=-1 ,
		hostel_name="None"
	)
	
	db.hostel_mapping.insert(
		hostel_id=0 ,
		hostel_name="Himadri"
	)
	
	db.hostel_mapping.insert(
		hostel_id=1 ,
		hostel_name="Kailash"
	)
	
	db.hostel_mapping.insert(
		hostel_id=2 ,
		hostel_name="Satpura"
	)
	
	db.hostel_mapping.insert(
		hostel_id=3 ,
		hostel_name="Girnar"
	)
	
	db.hostel_mapping.insert(
		hostel_id=4 ,
		hostel_name="Udaigiri"
	)
	
	db.hostel_mapping.insert(
		hostel_id=5 ,
		hostel_name="Zanskar"
	)
	
	db.hostel_mapping.insert(
		hostel_id=6 ,
		hostel_name="Jwalamukhi"
	)
	
	db.hostel_mapping.insert(
		hostel_id=7 ,
		hostel_name="Karakoram"
	)
	
	db.hostel_mapping.insert(
		hostel_id=8 ,
		hostel_name="Kumaon"
	)
	
	db.hostel_mapping.insert(
		hostel_id=9 ,
		hostel_name="Nilgiri"
	)
	
	db.hostel_mapping.insert(
		hostel_id=10 ,
		hostel_name="Vindhayachal"
	)
	
	db.hostel_mapping.insert(
		hostel_id=11 ,
		hostel_name="Aravali"
	)
	
	db.hostel_mapping.insert(
		hostel_id=12 ,
		hostel_name="Shivalik"
	)

	# db.notifications.insert(
	# 	complaint_id="i_123",
	# 	src_user_id="a1234",
	# 	dest_user_id="cs1140205",
	# 	description="time pass",  
	# )

	# db.notifications.insert(
	# 	complaint_id="i_1",
	# 	src_user_id="cs1130231",
	# 	dest_user_id="cs5140462",
	# 	description="Test notification 1"
	# )
	
	# db.notifications.insert(
	# 	complaint_id="i_2",
	# 	src_user_id="cs5140462",
	# 	dest_user_id="cs5140462",
	# 	description="Test notification 2 for complaint 2"
	# )
	
	# db.notifications.insert(
	# 	complaint_id="i_3",
	# 	src_user_id="cs1140205",
	# 	dest_user_id="cs5140462",
	# 	description="Test notification 3 for complaint 3"
	# )

	# db.indiv_complaints.insert(
	# 	complaint_id="i_1",
	# 	username="cs5140462",
	# 	complaint_type=1,
	# 	complaint_content="Complaint number 1",
	# 	extra_info="Extra info for comp 1",
	# 	admin_id="a1234"
	# )

	# db.indiv_complaints.insert(
	# 	complaint_id="i_2",
	# 	username="cs5140462",
	# 	complaint_type=1,
	# 	complaint_content="Complaint number 2",
	# 	extra_info="Extra info for comp 2",
	# 	admin_id="a1234"
	# )

	# db.indiv_complaints.insert(
	# 	complaint_id="i_3",
	# 	username="cs5140462",
	# 	complaint_type=1,
	# 	complaint_content="Complaint number 3",
	# 	extra_info="Extra info for comp 3",
	# 	admin_id="a1234"
	# )

	# db.complaint_user_mapping.insert(
	# 	complaint_id="i_1",
	# 	user_id="cs5140462"
	# )
	# db.complaint_user_mapping.insert(
	# 	complaint_id="i_2",
	# 	user_id="cs5140462"
	# )
	# db.complaint_user_mapping.insert(
	# 	complaint_id="i_3",
	# 	user_id="cs5140462"
	# )

	# db.hostel_complaints.insert(
	# 	complaint_id="h_1",
	# 	username="cs5140462",
	# 	complaint_content="Hostel complaint 1",
	# 	extra_info="Details of complaint",
	# 	complaint_type=2,
	# 	admin_id="a12345",
	# 	hostel='2'
	# )

	# db.complaint_user_mapping.insert(
	# 	complaint_id="h_1",
	# 	user_id="cs5140462"
	# )

	# db.complaint_user_mapping.insert(
	# 	complaint_id="h_1",
	# 	user_id="a12345"
	# )
	
	# db.insti_complaints.insert(
	# 	complaint_id="in_1",
	# 	username="cs5140462",
	# 	complaint_content="Institute complaint 1",
	# 	extra_info="Details of complaint",
	# 	complaint_type=2,
	# 	admin_id="a12345",
	# 	anonymous=1,
	# )

	# db.complaint_user_mapping.insert(
	# 	complaint_id="in_1",
	# 	user_id="cs5140462"
	# )

	# db.complaint_user_mapping.insert(
	# 	complaint_id="in_1",
	# 	user_id="a12345"
	# )

	# ## create 7 courses
	# db.courses.insert(
	#     name="Design Practices in Computer Science",
	#     code="cop290",
	#     description="Design Practices in Computer Science.",
	#     credits=3,
	#     l_t_p="0-0-6"
	# )

	# db.courses.insert(
	#     name="Wireless Networks",
	#     code="csl838",
	#     description="PHY and MAC layer concepts in wireless networking",
	#     credits=3,
	#     l_t_p="2-0-2"
	# )

	# db.courses.insert(
	#     name="Software Engineering",
	#     code="col740",
	#     description="Introduction to the concepts of Software Design and Engineering.",
	#     credits=4,
	#     l_t_p="3-0-2"
	# )

	# db.courses.insert(
	#     name="Cloud Computing and Virtualisation",
	#     code="csl732",
	#     description="Introduction to Cloud Computing and Virtualisation.",
	#     credits=4,
	#     l_t_p="3-0-2"
	# )

	# db.courses.insert(
	#     name="Parallel Programming",
	#     code="col380",
	#     description="Introduction to concurrent systems and programming style.",
	#     credits=4,
	#     l_t_p="3-0-2"
	# )

	# db.courses.insert(
	#     name="Computer Graphics",
	#     code="csl781",
	#     description="Computer Graphics.",
	#     credits=4,
	#     l_t_p="3-0-2"
	# )


	# db.courses.insert(
	#     name="Advanced Computer Graphics",
	#     code="csl859",
	#     description="Graduate course on Advanced Computer Graphics",
	#     credits=4,
	#     l_t_p="3-0-2"
	# )




	# ## create 7 registered courses
	# db.registered_courses.insert(    
	#     course_id=1,
	#     professor=5,
	#     year_=2016,
	#     semester=2,
	#     starting_date=datetime(2016,1,1),
	#     ending_date=datetime(2016,5,10),
	# )

	# db.registered_courses.insert(
	#     course_id=2,
	#     professor=5,
	#     year_=2016,
	#     semester=2,
	#     starting_date=datetime(2016,1,1),
	#     ending_date=datetime(2016,5,10),
	# )

	# db.registered_courses.insert(
	#     course_id=3,
	#     professor=6,
	#     year_=2016,
	#     semester=2,
	#     starting_date=datetime(2016,1,1),
	#     ending_date=datetime(2016,5,10),
	# )

	# db.registered_courses.insert(
	#     course_id=4,
	#     professor=6,
	#     year_=2016,
	#     semester=2,
	#     starting_date=datetime(2016,1,1),
	#     ending_date=datetime(2016,5,10),
	# )

	# db.registered_courses.insert(
	#     course_id=5,
	#     professor=7,
	#     year_=2016,
	#     semester=2,
	#     starting_date=datetime(2016,1,1),
	#     ending_date=datetime(2016,5,10),
	# )

	# db.registered_courses.insert(
	#     course_id=6,
	#     professor=7,
	#     year_=2016,
	#     semester=2,
	#     starting_date=datetime(2016,1,1),
	#     ending_date=datetime(2016,5,10),
	# )

	# db.registered_courses.insert(
	#     course_id=7,
	#     professor=7,
	#     year_=2016,
	#     semester=1,
	#     starting_date=datetime(2014,7,1),
	#     ending_date=datetime(2014,12,10),
	# )

	# ## register 3 students for 5 courses each out of 7 registered courses
	# db.student_registrations.insert(student_id=1,registered_course_id=3)
	# db.student_registrations.insert(student_id=1,registered_course_id=2)
	# db.student_registrations.insert(student_id=1,registered_course_id=1)
	# db.student_registrations.insert(student_id=1,registered_course_id=4)
	# db.student_registrations.insert(student_id=1,registered_course_id=5)
	# db.student_registrations.insert(student_id=2,registered_course_id=3)
	# db.student_registrations.insert(student_id=2,registered_course_id=4)
	# db.student_registrations.insert(student_id=2,registered_course_id=6)
	# db.student_registrations.insert(student_id=2,registered_course_id=7)
	# db.student_registrations.insert(student_id=2,registered_course_id=1)
	# db.student_registrations.insert(student_id=3,registered_course_id=3)
	# db.student_registrations.insert(student_id=3,registered_course_id=1)
	# db.student_registrations.insert(student_id=3,registered_course_id=5)
	# db.student_registrations.insert(student_id=3,registered_course_id=6)
	# db.student_registrations.insert(student_id=3,registered_course_id=2)
	# db.student_registrations.insert(student_id=4,registered_course_id=3)
	# db.student_registrations.insert(student_id=4,registered_course_id=4)
	# db.student_registrations.insert(student_id=4,registered_course_id=5)
	# db.student_registrations.insert(student_id=4,registered_course_id=7)
	# db.student_registrations.insert(student_id=4,registered_course_id=1)

	# ## create 3 assignments in Design Practices course
	# db.events.insert(
	#     registered_course_id=1,
	#     type_=0,
	#     name="Project Submission 1: Draft Requirement Document",
	#     description="<p><br></p><p>Organise 2 hr meeting of the team to</p><p>-Choose one of the Projects discussed in the class</p><p>-Discuss the specification of the selected project. Identify the aspects to be explored by team members&nbsp;</p><p>-Document the discussion and the initial specs of the project</p><p><br></p><p>Organise 2nd 2 hr meeting &nbsp;to</p><p>-Share the homework done by each team member</p><p>-Discuss and finalise the specs of the projects</p><p>-Prepare 1 or 2 page document on the draft project specification&nbsp;</p><p><br></p><p>Submit the draft Project Requirement Document by Wednesday mid night.</p><p>Add title of the project in the group excel sheet</p>",
	#     created_at=datetime.now(),
	#     deadline=datetime.now()-timedelta(days=-7),
	#     late_days_allowed=0
	# )

	# db.events.insert(
	#     registered_course_id=1,
	#     type_=0,
	#     name="Project Submission 2: Requirement Document in IEEE template format",
	#     description="<p>Submission Deadline 20 Feb Midnight.</p><p id='yui_3_17_2_3_1431040674495_308'>Recommended Process</p><p>-Meeting1 &nbsp;</p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Compete listing &nbsp;of User requirements</p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Create System Architecture</p><p id='yui_3_17_2_3_1431040674495_309'>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Identify Use cases, Users, draw Use Case Diagram<br></p><p>-Meeting2</p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Translate user requirement into system requirements</p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Discuss and document Use cases including relevant Models</p><p>-Meeting3&nbsp;</p><p>&nbsp; &nbsp; &nbsp; &nbsp; Discuss each section of the IEEE template&nbsp;</p><p>&nbsp; &nbsp; &nbsp; &nbsp; Create Document as per IEEE template</p><p><br></p><p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p><p>&nbsp;</p><p><br></p>",
	#     created_at=datetime.now(),
	#     deadline=datetime.now()-timedelta(days=-7),
	#     late_days_allowed=2
	# )

	# db.events.insert(
	#     registered_course_id=1,
	#     type_=0,
	#     name="Project Submission 3 : Detailed Design Document",
	#     description="<p>Based on the Requirement Document, a detailed design document</p><p>will be created by each group.</p><p>It should have the following components</p><p>-Project Overview</p><p>-Architectural design with well identified Modules</p><p>-Modules specification &amp; its APIs</p><p>-Database Design</p><p>-User Interface Design</p><p>-Module internal data structures and processing if needed.</p><p>-Aprorpriate Diagrams as necessary</p><p>-Any other information as necessary</p><p>Design document should be complete from all aspects ( i.e Requirement &amp; design document should be adequate for any other programming team to develop the system without may further input)</p><p>You may use any apropriate format for this design document</p><p>Submission date 29th March.</p><p><br></p><p><br></p>",
	#     created_at=datetime.now(),
	#     deadline=datetime.now()-timedelta(days=-7),
	#     late_days_allowed=3
	# )

	# ## Grades
	# db.grades.insert(user_id=1, registered_course_id=1, name="Assignment 1", score=15, out_of=15, weightage=10)
	# db.grades.insert(user_id=1, registered_course_id=1, name="Assignment 2", score=10, out_of=20, weightage=15)
	# db.grades.insert(user_id=1, registered_course_id=1, name="Minor 1", score=25, out_of=30, weightage=25)

	# db.grades.insert(user_id=2, registered_course_id=1, name="Assignment 1", score=15, out_of=15, weightage=10)
	# db.grades.insert(user_id=2, registered_course_id=1, name="Assignment 2", score=18, out_of=20, weightage=15)
	# db.grades.insert(user_id=2, registered_course_id=1, name="Minor 1", score=20, out_of=30, weightage=25)

	# db.grades.insert(user_id=3, registered_course_id=1, name="Assignment 1", score=15, out_of=15, weightage=10)
	# db.grades.insert(user_id=3, registered_course_id=1, name="Assignment 2", score=14, out_of=20, weightage=15)
	# db.grades.insert(user_id=3, registered_course_id=1, name="Minor 1", score=23, out_of=30, weightage=25)

	# db.grades.insert(user_id=4, registered_course_id=1, name="Assignment 1", score=15, out_of=15, weightage=10)
	# db.grades.insert(user_id=4, registered_course_id=1, name="Assignment 2", score=20, out_of=20, weightage=15)
	# db.grades.insert(user_id=4, registered_course_id=1, name="Minor 1", score=15, out_of=30, weightage=25)

	# ## create 4 threads in Different courses


	# ## Create Static Variables
	# db.static_vars.insert(
	#     name="current_year",
	#     int_value=2016,
	#     string_value="2016"
	# )

	# db.static_vars.insert(
	#     name="current_sem",
	#     int_value=2,
	#     string_value="2"
	# )
# def api():
# 	return """
# Moodle Plus API (ver 1.0)
# -------------------------

# Url: /default/login.json
# Input params:
# 	userid: (string)
# 	password: (string)
# Output params:
# 	success: (boolean) True if login success and False otherwise
# 	user: (json) User details if login is successful otherwise False


# Url: /default/logout.json
# Input params:
# Output params:
# 	success: (boolean) True if logout successful and False otherwise


# Url: /courses/list.json
# Input params:
# Output params:
# 	current_year: (int)
# 	current_sem: (int) 0 for summer, 1 break, 2 winter
# 	courses: (List) list of courses
# 	user: (dictionary) user details

# Url: /threads/new.json
# Input params:
# 	title: (string) can't be empty
# 	description: (string) can't be empty
# 	course_code: (string) must be a registered courses
# Output params:
# 	success: (bool) True or False depending on whether thread was posted
# 	thread_id: (bool) id of new thread created

# 	"""
