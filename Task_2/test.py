robotstate = ['start','SearchingHuman','NoHuman', 'Req_Destination','Search_Destination',\
              'No_Destination', 'Drive_to_Destination','Task_Finished']



destination_received = False #In interrupt'
destination = 'P'
LookforHuman()
AligntoHuman(position)



Interrupt to Handle destinations

Start
Stop


				result = LookforHuman()
				if result != -1:
                                    AligntoHuman(result)
                                    robotstate = 'Req_Destination'
