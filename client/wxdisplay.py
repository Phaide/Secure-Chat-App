# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainMenu
###########################################################################

class MainMenu ( wx.Frame ):

	def __init__( self, parent, o_node ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Secure chat app", pos = wx.DefaultPosition, size = wx.Size( 350,375 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 350,375 ), wx.DefaultSize )

		mainMenu_bSizer = wx.BoxSizer( wx.VERTICAL )

		info_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Info" ), wx.VERTICAL )

		serverStatus_bSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.serverStatusInfo_staticText = wx.StaticText( info_sbSizer.GetStaticBox(), wx.ID_ANY, u"Listening status: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.serverStatusInfo_staticText.Wrap( -1 )

		self.serverStatusInfo_staticText.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.serverStatusInfo_staticText.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )

		serverStatus_bSizer.Add( self.serverStatusInfo_staticText, 0, wx.ALL, 5 )

		self.serverStatus_staticText = wx.StaticText( info_sbSizer.GetStaticBox(), wx.ID_ANY, u"Down", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.serverStatus_staticText.Wrap( -1 )

		self.serverStatus_staticText.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.serverStatus_staticText.SetForegroundColour( wx.Colour( 255, 0, 0 ) )

		serverStatus_bSizer.Add( self.serverStatus_staticText, 0, wx.ALL, 5 )


		info_sbSizer.Add( serverStatus_bSizer, 1, wx.EXPAND, 5 )

		nodeName_bSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.nodeNameInfo_staticText = wx.StaticText( info_sbSizer.GetStaticBox(), wx.ID_ANY, u"Your name : ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.nodeNameInfo_staticText.Wrap( -1 )

		nodeName_bSizer.Add( self.nodeNameInfo_staticText, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

		self.nodeName_staticText = wx.StaticText( info_sbSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.nodeName_staticText.Wrap( -1 )

		self.nodeName_staticText.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		nodeName_bSizer.Add( self.nodeName_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		info_sbSizer.Add( nodeName_bSizer, 1, wx.EXPAND, 5 )


		mainMenu_bSizer.Add( info_sbSizer, 0, wx.EXPAND, 5 )

		rsaKeys_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"RSA Keys" ), wx.VERTICAL )

		self.rsaPublicKeyStatus_staticText = wx.StaticText( rsaKeys_sbSizer.GetStaticBox(), wx.ID_ANY, u"RSA PublicKey:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.rsaPublicKeyStatus_staticText.Wrap( -1 )

		rsaKeys_sbSizer.Add( self.rsaPublicKeyStatus_staticText, 0, wx.ALL, 5 )

		self.publicKey_filePicker = wx.FilePickerCtrl( rsaKeys_sbSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select an RSA PublicKey file", u"*.pem", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		self.publicKey_filePicker.SetToolTip( u"Select an RSA PublicKey file" )

		rsaKeys_sbSizer.Add( self.publicKey_filePicker, 0, wx.ALL|wx.EXPAND, 5 )

		self.rsaPrivateKeyStatus_staticText = wx.StaticText( rsaKeys_sbSizer.GetStaticBox(), wx.ID_ANY, u"RSA PrivateKey: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.rsaPrivateKeyStatus_staticText.Wrap( -1 )

		rsaKeys_sbSizer.Add( self.rsaPrivateKeyStatus_staticText, 0, wx.ALL, 5 )

		self.privateKey_filePicker = wx.FilePickerCtrl( rsaKeys_sbSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select an RSA PrivateKey file", u"*.pem", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		self.privateKey_filePicker.SetToolTip( u"Select an RSA PrivateKey file" )

		rsaKeys_sbSizer.Add( self.privateKey_filePicker, 0, wx.ALL|wx.EXPAND, 5 )

		self.createNewKeyPair_button = wx.Button( rsaKeys_sbSizer.GetStaticBox(), wx.ID_ANY, u"Create a new key pair", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.createNewKeyPair_button.SetToolTip( u"Create a new pair of RSA keys" )

		rsaKeys_sbSizer.Add( self.createNewKeyPair_button, 0, wx.ALL|wx.EXPAND, 5 )


		mainMenu_bSizer.Add( rsaKeys_sbSizer, 0, wx.EXPAND, 5 )

		chat_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Chat" ), wx.VERTICAL )

		self.showConversations_Button = wx.Button( chat_sbSizer.GetStaticBox(), wx.ID_ANY, u"Chat with other nodes", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.showConversations_Button.Enable( False )

		chat_sbSizer.Add( self.showConversations_Button, 0, wx.ALL|wx.EXPAND, 5 )


		mainMenu_bSizer.Add( chat_sbSizer, 0, wx.EXPAND, 5 )


		self.SetSizer( mainMenu_bSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.publicKey_filePicker.Bind( wx.EVT_FILEPICKER_CHANGED, self.load_public_key )
		self.privateKey_filePicker.Bind( wx.EVT_FILEPICKER_CHANGED, self.load_private_key )
		self.createNewKeyPair_button.Bind( wx.EVT_BUTTON, self.open_pair_creation_window )
		self.showConversations_Button.Bind( wx.EVT_BUTTON, self.show_conversations )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def load_public_key( self, event ):
		event.Skip()

	def load_private_key( self, event ):
		event.Skip()

	def open_pair_creation_window( self, event ):
		event.Skip()

	def show_conversations( self, event ):
		event.Skip()


###########################################################################
## Class CreateNewKeyPair
###########################################################################

class CreateNewKeyPair ( wx.Frame ):

	def __init__( self, parent, o_node ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Create a new key pair", pos = wx.DefaultPosition, size = wx.Size( 525,275 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 525,275 ), wx.DefaultSize )

		createNewKeyPair_bSizer = wx.BoxSizer( wx.VERTICAL )

		pairLocation_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Location" ), wx.VERTICAL )

		self.pairCreationInfo1_staticText = wx.StaticText( pairLocation_sbSizer.GetStaticBox(), wx.ID_ANY, u"Note: as soon as you select a directory, the creation will launch.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pairCreationInfo1_staticText.Wrap( -1 )

		pairLocation_sbSizer.Add( self.pairCreationInfo1_staticText, 0, wx.ALL, 5 )

		self.keyPairLocation_dirPicker = wx.DirPickerCtrl( pairLocation_sbSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a folder where the keys will be stored", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		pairLocation_sbSizer.Add( self.keyPairLocation_dirPicker, 0, wx.ALL|wx.EXPAND, 5 )

		self.pairCreationInfo2_staticText = wx.StaticText( pairLocation_sbSizer.GetStaticBox(), wx.ID_ANY, u"Files will be named \"private_[ID].pem\" and \"public_[ID].pem\".", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pairCreationInfo2_staticText.Wrap( -1 )

		pairLocation_sbSizer.Add( self.pairCreationInfo2_staticText, 0, wx.ALL, 5 )


		createNewKeyPair_bSizer.Add( pairLocation_sbSizer, 0, wx.ALL|wx.EXPAND, 5 )

		keyPairCreationLoading_bSizer = wx.BoxSizer( wx.VERTICAL )

		self.loadingTitle_staticText = wx.StaticText( self, wx.ID_ANY, u"Creating the keys...", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_ELLIPSIZE_END )
		self.loadingTitle_staticText.Wrap( -1 )

		self.loadingTitle_staticText.SetFont( wx.Font( 18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.loadingTitle_staticText.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )

		keyPairCreationLoading_bSizer.Add( self.loadingTitle_staticText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.loadingInfo1_staticText = wx.StaticText( self, wx.ID_ANY, u"Important note : the process can take up to a few minutes to complete. Please be patient :)", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_ELLIPSIZE_END )
		self.loadingInfo1_staticText.Wrap( -1 )

		self.loadingInfo1_staticText.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )

		keyPairCreationLoading_bSizer.Add( self.loadingInfo1_staticText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.loadingInfo2_staticText = wx.StaticText( self, wx.ID_ANY, u"The window might freeze and even seem to crash, don't close it, it's working.", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_ELLIPSIZE_END )
		self.loadingInfo2_staticText.Wrap( -1 )

		self.loadingInfo2_staticText.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )

		keyPairCreationLoading_bSizer.Add( self.loadingInfo2_staticText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		createNewKeyPair_bSizer.Add( keyPairCreationLoading_bSizer, 1, wx.EXPAND, 5 )


		self.SetSizer( createNewKeyPair_bSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.keyPairLocation_dirPicker.Bind( wx.EVT_DIRPICKER_CHANGED, self.create_key_pair )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def create_key_pair( self, event ):
		event.Skip()


###########################################################################
## Class ReceivedMessages
###########################################################################

class ReceivedMessages ( wx.Frame ):

	def __init__( self, parent, o_node ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"See all conversations", pos = wx.DefaultPosition, size = wx.Size( 548,562 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 300,300 ), wx.DefaultSize )

		receivedMessages_bSizer = wx.BoxSizer( wx.VERTICAL )

		self.filterNodes_searchCtrl = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.filterNodes_searchCtrl.ShowSearchButton( True )
		self.filterNodes_searchCtrl.ShowCancelButton( True )
		self.filterNodes_searchCtrl.SetToolTip( u"Search for a node" )

		receivedMessages_bSizer.Add( self.filterNodes_searchCtrl, 0, wx.ALL|wx.EXPAND, 5 )

		chatContainerMain_bSizer = wx.BoxSizer( wx.HORIZONTAL )

		chatContainer_bSizer = wx.BoxSizer( wx.VERTICAL )

		node1_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"node1" ), wx.HORIZONTAL )

		self.node1_lastConvSnippet_staticText = wx.StaticText( node1_sbSizer.GetStaticBox(), wx.ID_ANY, u"Thanks I like that too", wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_END )
		self.node1_lastConvSnippet_staticText.Wrap( -1 )

		node1_sbSizer.Add( self.node1_lastConvSnippet_staticText, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.node1_lastConvDate_staticText = wx.StaticText( node1_sbSizer.GetStaticBox(), wx.ID_ANY, u"11:16 14/04/2020", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.node1_lastConvDate_staticText.Wrap( -1 )

		node1_sbSizer.Add( self.node1_lastConvDate_staticText, 0, wx.ALIGN_RIGHT|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.node1_button = wx.Button( node1_sbSizer.GetStaticBox(), wx.ID_ANY, u"Open", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		node1_sbSizer.Add( self.node1_button, 0, wx.ALL, 5 )


		chatContainer_bSizer.Add( node1_sbSizer, 0, wx.ALL|wx.EXPAND, 5 )

		node2_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"node2" ), wx.HORIZONTAL )

		self.node2_lastConvSnippet_staticText = wx.StaticText( node2_sbSizer.GetStaticBox(), wx.ID_ANY, u"Hey, this is another test and this time the text is too long to be display entirely, what will happen ?", wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_END )
		self.node2_lastConvSnippet_staticText.Wrap( -1 )

		node2_sbSizer.Add( self.node2_lastConvSnippet_staticText, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.node2_lastConvDate_staticText = wx.StaticText( node2_sbSizer.GetStaticBox(), wx.ID_ANY, u"19:04 13/04/2020", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.node2_lastConvDate_staticText.Wrap( -1 )

		node2_sbSizer.Add( self.node2_lastConvDate_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.node2_button = wx.Button( node2_sbSizer.GetStaticBox(), wx.ID_ANY, u"Open", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		node2_sbSizer.Add( self.node2_button, 0, wx.ALL, 5 )


		chatContainer_bSizer.Add( node2_sbSizer, 0, wx.ALL|wx.EXPAND, 5 )


		chatContainerMain_bSizer.Add( chatContainer_bSizer, 1, wx.EXPAND, 5 )

		self.conversations_scrollBar = wx.ScrollBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SB_VERTICAL )
		chatContainerMain_bSizer.Add( self.conversations_scrollBar, 0, wx.ALL|wx.EXPAND, 5 )


		receivedMessages_bSizer.Add( chatContainerMain_bSizer, 1, wx.EXPAND, 5 )

		newChat_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"New conversation" ), wx.VERTICAL )

		recipient_bSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.recipient_staticText = wx.StaticText( newChat_sbSizer.GetStaticBox(), wx.ID_ANY, u"Send to:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.recipient_staticText.Wrap( -1 )

		recipient_bSizer.Add( self.recipient_staticText, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		recipient_choiceChoices = [ u"node3", u"node4" ]
		self.recipient_choice = wx.Choice( newChat_sbSizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, recipient_choiceChoices, 0 )
		self.recipient_choice.SetSelection( 0 )
		recipient_bSizer.Add( self.recipient_choice, 1, wx.ALL, 5 )


		newChat_sbSizer.Add( recipient_bSizer, 0, wx.EXPAND, 5 )

		self.message_staticText = wx.StaticText( newChat_sbSizer.GetStaticBox(), wx.ID_ANY, u"Message", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.message_staticText.Wrap( -1 )

		newChat_sbSizer.Add( self.message_staticText, 0, 0, 5 )

		self.newChatMessage_textCtrl = wx.TextCtrl( newChat_sbSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_AUTO_URL|wx.TE_BESTWRAP|wx.TE_CHARWRAP|wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_RICH|wx.TE_RICH2|wx.TE_WORDWRAP )
		self.newChatMessage_textCtrl.SetMinSize( wx.Size( -1,50 ) )

		newChat_sbSizer.Add( self.newChatMessage_textCtrl, 1, wx.ALL|wx.EXPAND, 5 )

		self.sendNewChat_button = wx.Button( newChat_sbSizer.GetStaticBox(), wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		newChat_sbSizer.Add( self.sendNewChat_button, 0, wx.ALL, 5 )


		receivedMessages_bSizer.Add( newChat_sbSizer, 0, wx.EXPAND, 5 )


		self.SetSizer( receivedMessages_bSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.filterNodes_searchCtrl.Bind( wx.EVT_TEXT_ENTER, self.filter_search )
		self.node1_button.Bind( wx.EVT_BUTTON, self.open_chat_id )
		self.sendNewChat_button.Bind( wx.EVT_BUTTON, self.send_message_to_new_node )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def filter_search( self, event ):
		event.Skip()

	def open_chat_id( self, event ):
		event.Skip()

	def send_message_to_new_node( self, event ):
		event.Skip()


###########################################################################
## Class Conversation
###########################################################################

class Conversation ( wx.Frame ):

	def __init__( self, parent, o_node ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Conversation - node1", pos = wx.DefaultPosition, size = wx.Size( 624,320 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		conversation_bSizer = wx.BoxSizer( wx.HORIZONTAL )

		messagesMain_bSizer8 = wx.BoxSizer( wx.VERTICAL )

		messages_bSizer = wx.BoxSizer( wx.VERTICAL )

		message_1_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"node1" ), wx.HORIZONTAL )

		self.messageContent_1_staticText = wx.StaticText( message_1_sbSizer.GetStaticBox(), wx.ID_ANY, u"Hey, how are you doing today ? I eat pastas on a daily basis though", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.messageContent_1_staticText.Wrap( -1 )

		message_1_sbSizer.Add( self.messageContent_1_staticText, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

		self.messageTimestamp_1_staticText = wx.StaticText( message_1_sbSizer.GetStaticBox(), wx.ID_ANY, u"11:12 14/04/2020", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.messageTimestamp_1_staticText.Wrap( -1 )

		message_1_sbSizer.Add( self.messageTimestamp_1_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		messages_bSizer.Add( message_1_sbSizer, 0, wx.ALL|wx.EXPAND, 5 )

		message_2_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"me (node5)" ), wx.HORIZONTAL )

		self.messageContent_2_staticText = wx.StaticText( message_2_sbSizer.GetStaticBox(), wx.ID_ANY, u"Nice, I eat bolognese along with banana", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.messageContent_2_staticText.Wrap( -1 )

		message_2_sbSizer.Add( self.messageContent_2_staticText, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

		self.messageTimestamp_2_staticText = wx.StaticText( message_2_sbSizer.GetStaticBox(), wx.ID_ANY, u"11:15 14/04/2020", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.messageTimestamp_2_staticText.Wrap( -1 )

		message_2_sbSizer.Add( self.messageTimestamp_2_staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		messages_bSizer.Add( message_2_sbSizer, 0, wx.ALL|wx.EXPAND, 5 )

		message_3_sbSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"node1" ), wx.HORIZONTAL )

		self.messageContent_3_staticText = wx.StaticText( message_3_sbSizer.GetStaticBox(), wx.ID_ANY, u"Thanks I like that too", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.messageContent_3_staticText.Wrap( -1 )

		message_3_sbSizer.Add( self.messageContent_3_staticText, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

		self.messageTimestamp_3_staticText = wx.StaticText( message_3_sbSizer.GetStaticBox(), wx.ID_ANY, u"11:16 14/04/2020", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.messageTimestamp_3_staticText.Wrap( -1 )

		message_3_sbSizer.Add( self.messageTimestamp_3_staticText, 0, wx.ALL, 5 )


		messages_bSizer.Add( message_3_sbSizer, 0, wx.ALL|wx.EXPAND, 5 )


		messagesMain_bSizer8.Add( messages_bSizer, 1, wx.EXPAND, 5 )

		newMessage_bSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.newMessage_textCtrl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		newMessage_bSizer.Add( self.newMessage_textCtrl, 1, wx.ALL|wx.EXPAND, 5 )

		self.sendMessage_button = wx.Button( self, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		newMessage_bSizer.Add( self.sendMessage_button, 0, wx.ALL, 5 )


		messagesMain_bSizer8.Add( newMessage_bSizer, 0, wx.EXPAND, 5 )


		conversation_bSizer.Add( messagesMain_bSizer8, 1, wx.EXPAND, 5 )

		self.messages_scrollBar = wx.ScrollBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SB_VERTICAL )
		conversation_bSizer.Add( self.messages_scrollBar, 0, wx.EXPAND, 5 )


		self.SetSizer( conversation_bSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.sendMessage_button.Bind( wx.EVT_BUTTON, self.send_message_to_current_node )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def send_message_to_current_node( self, event ):
		event.Skip()
