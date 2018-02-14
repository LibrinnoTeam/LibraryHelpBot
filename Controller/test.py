import os
from datetime import datetime
from datetime import timedelta

from Controller.controller import Controller
from DataBase.BDmanagement import BDManagement
from DataBase.UsersAndDocumentObjects.Patron import Patron
#There is at least one patron and one librarian in the system. Patron p has no item. In the
#library, there are two copies of book b, which is not a reference book.
#
def first_test(cntrl):

	clear_tables(cntrl)

	test_user = {'id':1,'name':'test','address':'tEsT','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	cntrl.check_out_doc(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','book',test_book['title'])[0])
	book_db = dict(zip(['id','title','authors','overview','count','free_count','price'],book_db_t))
	order_id = int(eval(user_db['current_docs'])[0])
	user_book_id = cntrl.BDmanager.get_by('id','orders',order_id)[0][3]

	is_user_have_book = user_book_id == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	if  not is_user_have_book or not is_book_free_count_decremented:
		return 'Can`t check out book, is user have book: ' + str(is_user_have_book) + ' , is book free count decremented: ' + str(is_book_free_count_decremented), False

	return 'OK', True


def second_test(cntrl):
	
	clear_tables(cntrl)

	id_book_A = 1
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	cntrl.BDmanager.add_patron(Patron(**test_user))
	can_get_book = cntrl.check_out_doc(test_user['id'],id_book_A)

	if can_get_book[0]:
		return 'Book found', False

	return 'OK', True


def third_test(cntrl):

	clear_tables(cntrl)

	test_user = {'id':1,'name':'test','address':'test','status':'Faculty','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	cntrl.check_out_doc(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','book',test_book['title'])[0])
	book_db = dict(zip(['id','title','authors','overview','count','free_count','price','keywords'],book_db_t))
	order_id = int(eval(user_db['current_docs'])[0])
	order = dict(zip(['id','time','table','userId','docId','out_of_time'],list(cntrl.BDmanager.get_by('id','orders',order_id)[0])))
	#TODO: check time  

	order['time'] = datetime.strptime(order['time'],'%Y-%m-%d')
	order['out_of_time'] = datetime.strptime(order['out_of_time'],'%Y-%m-%d')

	is_user_have_book = order['docId'] == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	is_out_of_time_equality = order['out_of_time'] == order['time'] + timedelta(weeks = 4)
	if  not is_user_have_book or not is_book_free_count_decremented:
		return 'Can`t check out book, is user have book: ' + str(is_user_have_book) + ' , is book free count decremented: ' + str(is_book_free_count_decremented), False

	return 'OK', True


def fourth_test(cntrl):
	
	clear_tables(cntrl)

	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'best_seller':1,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	cntrl.check_out_doc(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','book',test_book['title'])[0])
	book_db = dict(zip(['id','title','authors','overview','count','free_count','price','keywords'],book_db_t))
	order_id = int(eval(user_db['current_docs'])[0])
	order = dict(zip(['id','time','table','userId','docId','out_of_time'],list(cntrl.BDmanager.get_by('id','orders',order_id)[0])))
	
	order['time'] = datetime.strptime(order['time'],'%Y-%m-%d')
	order['out_of_time'] = datetime.strptime(order['out_of_time'],'%Y-%m-%d') 

	is_user_have_book = order['docId'] == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	is_out_of_time_equality = order['out_of_time'] == order['time'] + timedelta(weeks = 2)
	if  not is_user_have_book or not is_book_free_count_decremented:
		return 'Can`t check out book, is user have book: ' + str(is_user_have_book) + ' , is book free count decremented: ' + str(is_book_free_count_decremented) + ', is out of time equality : ' +str(is_out_of_time_equality) , False

	return 'OK', True


def fifth_test(cntrl):

	clear_tables(cntrl)
	
	test_user_1 = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_user_2 = {'id':2,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_user_3 = {'id':3,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}

	cntrl.BDmanager.add_patron(Patron(**test_user_1))
	cntrl.BDmanager.add_patron(Patron(**test_user_2))
	cntrl.BDmanager.add_patron(Patron(**test_user_3))

	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}
	
	cntrl.add_book(**test_book)

	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	is_first_user_check_out = cntrl.check_out_doc(test_user_1['id'],book_id)
	is_second_user_check_out = cntrl.check_out_doc(test_user_3['id'],book_id)
	is_third_user_check_out = cntrl.check_out_doc(test_user_2['id'],book_id)
	
	if not is_first_user_check_out[0] or not is_second_user_check_out[0] or is_third_user_check_out[0]:
		return 'Is first user check out : ' + str(is_first_user_check_out) + ', is second user check out : ' + str(is_second_user_check_out) \
			+ ', is third user check out : '+ str(is_third_user_check_out), False

	return 'OK',True


def sixth_test(cntrl):

	clear_tables(cntrl)
	
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	first_copy = cntrl.check_out_doc(test_user['id'],book_id)
	second_copy = cntrl.check_out_doc(test_user['id'],book_id)

	if not first_copy[0] or second_copy[0]:
		return 'Can get two copies of book. First copy : ' + str(first_copy) + ', second copy : ' + str(second_copy), False

	return 'OK', True


def seventh_test(cntrl):

	clear_tables(cntrl)

	test_user_1 = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_user_2 = {'id':2,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}

	cntrl.BDmanager.add_patron(Patron(**test_user_1))
	cntrl.BDmanager.add_patron(Patron(**test_user_2))

	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}
	
	cntrl.add_book(**test_book)

	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	is_first_user_check_out = cntrl.check_out_doc(test_user_1['id'],book_id)
	is_second_user_check_out = cntrl.check_out_doc(test_user_2['id'],book_id)

	if not is_first_user_check_out[0] or not is_second_user_check_out[0]:
		return 'Is first user check out : ' + str(is_first_user_check_out) + ', is second user check out : ' + str(is_second_user_check_out), False

	return 'OK',True


def eighth_test(cntrl):

	clear_tables(cntrl)
	
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	cntrl.check_out_doc(test_user['id'],book_id,'book',3)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','book',test_book['title'])[0])
	book_db = dict(zip(['id','title','author','overview','count','free_count','price','keywords'],book_db_t))
	order_id = int(eval(user_db['current_docs'])[0])
	order = dict(zip(['id','time','table','userId','docId','out_of_time'],list(cntrl.BDmanager.get_by('id','orders',order_id)[0])))
	
	order['time'] = datetime.strptime(order['time'],'%Y-%m-%d')
	order['out_of_time'] = datetime.strptime(order['out_of_time'],'%Y-%m-%d')

	is_user_have_book = order['docId'] == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	is_out_of_time_equality = order['out_of_time'] == order['time'] + timedelta(weeks = 3)
	if  not is_user_have_book or not is_book_free_count_decremented:
		return 'Can`t check out book, is user have book: ' + str(is_user_have_book) + ' , is book free count decremented: ' + str(is_book_free_count_decremented) + ', is out of time equality : ' +str(is_out_of_time_equality) , False

	return 'OK', True


def ninth_test(cntrl):
	
	clear_tables(cntrl)

	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_book(**test_book)
	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	
	cntrl.check_out_doc(test_user['id'],book_id)
	
	user_db = cntrl.get_user(test_user['id'])
	book_db_t = list(cntrl.BDmanager.get_by('name','book',test_book['title'])[0])
	book_db = dict(zip(['id','title','authors','overview','count','free_count','price','keywords'],book_db_t))
	order_id = int(eval(user_db['current_docs'])[0])
	order = dict(zip(['id','time','table','userId','docId','out_of_time'],list(cntrl.BDmanager.get_by('id','orders',order_id)[0])))
	
	order['time'] = datetime.strptime(order['time'],'%Y-%m-%d')
	order['out_of_time'] = datetime.strptime(order['out_of_time'],'%Y-%m-%d') 

	is_user_have_book = order['docId'] == book_id 
	is_book_free_count_decremented = book_db['free_count'] == book_db['count'] - 1
	is_out_of_time_equality = order['out_of_time'] == order['time'] + timedelta(weeks = 2)
	if  not is_user_have_book or not is_book_free_count_decremented:
		return 'Can`t check out book, is user have book: ' + str(is_user_have_book) + ' , is book free count decremented: ' + str(is_book_free_count_decremented) + ', is out of time equality : ' +str(is_out_of_time_equality) , False

	return 'OK', True


def tenth_test(cntrl):

	clear_tables(cntrl)

	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}
	test_book_1 = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':''}
	test_book_2 = {'title': 'TEEST','overview':'TESTTEST','authors':'tEsT','count':0,'price':122,'keywords':''}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	
	cntrl.add_book(**test_book_1)
	cntrl.add_book(**test_book_2)

	book_id_1 = cntrl.BDmanager.get_by('name','book',test_book_1['title'])[0][0]
	book_id_2 = cntrl.BDmanager.get_by('name','book',test_book_2['title'])[0][0]

	regular_book = cntrl.check_out_doc(test_user['id'],book_id_1)
	references_book = cntrl.check_out_doc(test_user['id'],book_id_2)

	if  not regular_book[0] or references_book[0]:
		return 'Regular book : ' + str(regular_book) + ' , references book : ' + str(references_book), False

	return 'OK', True


def test_add_book(cntrl):

	clear_tables(cntrl)
	
	test_book_1 = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':0}
	test_book_2 = {'title': 'Test2','overview':'TESTTEST2','authors':'tEsT2','count':1,'price':1223,'keywords':0}
	
	cntrl.add_book(**test_book_1)
	cntrl.add_book(**test_book_2)

	is_in_db_first_book = check_in_db_books(cntrl.BDmanager,test_book_1)
	is_in_db_second_book = check_in_db_books(cntrl.BDmanager,test_book_2)
	if not is_in_db_first_book or not is_in_db_second_book:
		return 'Can`t add book in db. First book added: ' + str(is_in_db_first_book) + ' , Second book added : ' + str(is_in_db_second_book),False

	return 'OK',True


def test_registration_confirm_uptolibrarian(cntrl):
	
	clear_tables(cntrl)

	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987'}
	cntrl.registration(test_user)
	if not check_in_db_users(cntrl.BDmanager,'unconfirmed',test_user):
		return 'Can`t registrate',False
	
	cntrl.confirm_user(test_user['id'])
	in_unconfirmed_table = check_in_db_users(cntrl.BDmanager,'unconfirmed',test_user)
	in_patrons_table = check_in_db_users(cntrl.BDmanager,'patrons',test_user)
	if  in_unconfirmed_table or not in_patrons_table:
		return 'Can`t confirm user, in unconfirmed table: ' + str(in_unconfirmed_table) + ', in patrons table: ' + str(in_patrons_table),False

	cntrl.upto_librarian(test_user['id'])
	test_user['status'] = 'librarian'
	if check_in_db_users(cntrl.BDmanager,'patrons',test_user) or not check_in_db_users(cntrl.BDmanager,'librarians',test_user):
		return 'Can`t up to librarian',False

	return 'OK',True


def check_in_db_users(dbmanage,table,user):
	user_db_t = dbmanage.select_label(table,user['id'])
	if not user_db_t:
		return False
	
	user_db = {'id':user_db_t[0],'name':user_db_t[1],'phone':user_db_t[2],'address':user_db_t[3]}
	if table == 'patrons':
		user_db['address'] = user_db_t[3]
		user_db['phone'] = user_db_t[2]
		user_db['status'] = user_db_t[6]
	elif table == 'librarians':
		user_db['phone'] = user_db_t[3]
		user_db['address'] = user_db_t[2]
		user_db['status'] = user_db_t[4]
	elif table == 'unconfirmed':
		user_db['address'] = user_db_t[3]
		user_db['phone'] = user_db_t[2]
		user_db['status'] = user_db_t[4]
	for key in user.keys():
		if user[key] != user_db[key]:
			return False

	return True


def check_in_db_books(dbmanage,book):
	book_db_t = list(dbmanage.get_by('name','book',book['title'])[0])
	book_db = dict(zip(['id','title','authors','overview','count','free_count','price','keywords'],book_db_t))
	for key in book.keys():
		if book[key] != book_db[key]:
			print(key + " : " + str(book[key]) + ' != ' + str(book_db[key]))
			return False
	return True


def test_get_all_books(cntrl):

	clear_tables(cntrl)
	
	test_book_1 = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':0}
	test_book_2 = {'title': 'Test2','overview':'TESTTEST2','authors':'tEsT2','count':1,'price':1223,'keywords':0}
	
	cntrl.add_book(**test_book_1)
	cntrl.add_book(**test_book_2)

	books = cntrl.get_all_books()
	first_book = test_book_1['title'] == books[0]['title']
	second_book = test_book_2['title'] == books[1]['title']

	if not first_book or not second_book:
		return 'First book : ' + str(first_book) + ' Second book : ' + str(second_book),False

	cntrl.BDmanager.clear_table('book')

	return 'OK', True


def test_check_out_media(cntrl):

	clear_tables(cntrl)
	
	test_media = {'title':'Teste','authors':'XY','keywords':'oansedi','price':123,'best_seller':1,'count':1}
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}

	cntrl.add_media(**test_media)
	cntrl.BDmanager.add_patron(Patron(**test_user))

	media_id = cntrl.BDmanager.get_by('name','media',test_media['title'])
	
	if media_id == None:
		return 'Can`t add media to DB', False
	media_id = media_id[0][0]
	success,msg = cntrl.check_out_doc(test_user['id'],media_id,'media')
	if not success:
		return 'Can`t get book : ' + msg, False

	test_user = cntrl.get_user(test_user['id'])
	order = cntrl.BDmanager.select_label('orders',eval(test_user['current_docs'])[0])
	is_order_media = order[2] == 'media'
	is_ids_match = order[3] == media_id
	
	if not is_order_media or not is_ids_match:
		return 'is_order_media : ' + str(is_order_media) + ', is_ids_match : ' + str(is_ids_match), False

	return 'OK',True


def test_modify_doc(cntrl):

	clear_tables(cntrl)

	test_book = {'title': 'Test','overview':'TESTTEST','authors':'tEsT','count':2,'price':123,'keywords':0}
	cntrl.add_book(**test_book)

	book_id = cntrl.BDmanager.get_by('name','book',test_book['title'])[0][0]
	if book_id == None:
		return 'Can`t find book in db', False
	changes = {'id':book_id,'price':246,'author':'TTTTTTT'}
	cntrl.modify_document(changes,'book')
	try:
		price = cntrl.BDmanager.get_label('price','book',book_id)
		authors = cntrl.BDmanager.get_label('author','book',book_id)
		if price != changes['price'] or authors != changes['author']:
			return 'Can`t change document',False
		
		return 'OK',True
	except Exception:
		return 'Can`t find book in db', False


def test_return_doc(cntrl):
	
	test_media = {'title':'Teste','authors':'XY','keywords':'oansedi','price':123,'best_seller':1,'count':1}
	test_user = {'id':1,'name':'test','address':'test','status':'Student','phone':'987', 'history':[],'current_books':[]}

	cntrl.BDmanager.add_patron(Patron(**test_user))
	cntrl.add_media(**test_media)

	media_id = cntrl.BDmanager.get_by('name','media',test_media['title'])[0][0]

	if type(media_id) != type(1):
		return 'Can`t find document in db', False

	success,msg = cntrl.check_out_doc(test_user['id'],media_id,'media')
	
	if not success:
		return msg,False
	
	success, msg = cntrl.return_doc(test_user['id'],media_id)

	if not success:
		return msg,False
	
	user_current_docs = eval(cntrl.BDmanager.get_label('current_books','patrons',test_user['id']))
	media_count = cntrl.BDmanager.get_label('free_count','media',media_id)
	clear_currents_doc = user_current_docs == []
	count_of_media = media_count == test_media['count']
	if not clear_currents_doc or not count_of_media:
		return 'Can`t return book : Clear current doc ' + str(clear_currents_doc) + ', Count of media : ' + str(count_of_media), False
	return 'OK', True

def clear_tables(cntrl):
	cntrl.BDmanager.clear_table('media')
	cntrl.BDmanager.clear_table('librarians')
	cntrl.BDmanager.clear_table('article')
	cntrl.BDmanager.clear_table('book')
	cntrl.BDmanager.clear_table('patrons')
	cntrl.BDmanager.clear_table('orders')
	

def test_controller():

	cntrl = Controller('test.db')
	try:
		num_test_case = int(input("Enter test case : "))
		if num_test_case == 0:
			msg,err = first_test(cntrl)
			print('First test : ' + msg)
			msg,err = second_test(cntrl)
			print('Second test : ' + msg)
			msg,err = third_test(cntrl)
			print('Third test : ' + msg)
			msg,err = fourth_test(cntrl)
			print('Fourth test : ' + msg)
			msg,err = fifth_test(cntrl)
			print('Fifth test : ' + msg)
			msg,err = sixth_test(cntrl)
			print('Sixth test : ' + msg)
			msg,err = seventh_test(cntrl)
			print('Seventh test : ' + msg)
			msg,err = eighth_test(cntrl)
			print('Eighth test : ' + msg)
			msg,err = ninth_test(cntrl)
			print('Ninth test : ' + msg)
			msg,err = tenth_test(cntrl)
			print('Tenth test : ' + msg)
			msg,err = test_registration_confirm_uptolibrarian(cntrl)
			print('test_registration_confirm_uptolibrarian : ' + msg)
			msg,err = test_add_book(cntrl)
			print('test_add_book : ' + msg)
			msg,err = test_get_all_books(cntrl)
			print('test_get_all_books : ' + msg)
			msg,err = test_check_out_media(cntrl)
			print('test_check_out_media : ' + msg)
			msg,err = test_modify_doc(cntrl)
			print('test_modify_doc : ',msg)
			msg,err = test_return_doc(cntrl)
			print('test_return_doc : ',msg)
		elif num_test_case == 1:
			msg,err = first_test(cntrl)
			print('First test : ' + msg)
		elif num_test_case == 2:
			msg,err = second_test(cntrl)
			print('Second test : ' + msg)
		elif num_test_case == 3:
			msg,err = third_test(cntrl)
			print('Third test : ' + msg)
		elif num_test_case == 4:
			msg,err = fourth_test(cntrl)
			print('Fourth test : ' + msg)  
		elif num_test_case == 5:
			msg,err = fifth_test(cntrl)
			print('Fifth test : ' + msg)
		elif num_test_case == 6:
			msg,err = sixth_test(cntrl)
			print('Sixth test : ' + msg)
		elif num_test_case == 7:
			msg,err = seventh_test(cntrl)
			print('Seventh test : ' + msg)
		elif num_test_case == 8:
			msg,err = eighth_test(cntrl)
			print('Eighth test : ' + msg)
		elif num_test_case == 9:
			msg,err = ninth_test(cntrl)
			print('Ninth test : ' + msg)
		elif num_test_case == 10:
			msg,err = tenth_test(cntrl)
			print('Tenth test : ' + msg)
		elif num_test_case == 11:
			msg,err = test_registration_confirm_uptolibrarian(cntrl)
			print('test_registration_confirm_uptolibrarian : ' + msg)
		elif num_test_case == 12:
			msg,err = test_add_book(cntrl)
			print('test_add_book : ' + msg)
		elif num_test_case == 13:
			msg,err = test_get_all_books(cntrl)
			print('test_get_all_books : ' + msg)
		elif num_test_case == 14:
			msg,err = test_check_out_media(cntrl)
			print('test_check_out_media : ' + msg)
		elif num_test_case == 15:
			msg,err = test_modify_doc(cntrl)
			print('test_modify_doc : ',msg)
		elif num_test_case == 16:
			msg,err = test_return_doc(cntrl)
			print('test_return_doc : ',msg)
	except Exception as e:
		raise e
	finally:
		os.remove('test.db')

if __name__ == '__main__':
	test_controller()
