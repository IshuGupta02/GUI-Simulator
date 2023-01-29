f =  open("assets/L1DCache","r") 

queues = ['RDREQ','WRREQ','PBR_REQ','PBR_RSP','FILL','MISS','VICTIM','PRB_REQ','PBR_RESP','RDRESP']
cyc_data = []
for line in f:
    line = line.strip()
    cyc_num_start_index = line.find('Cycle$') + 6
    cyc_num_end_index = line.find('\t',cyc_num_start_index) - 1
    cyc_num = int(line[cyc_num_start_index:cyc_num_end_index+1])

    curr_cyc_data = []
    for queue in queues:
        data_st_ind = line.find(queue) + len(queue)
        queue_space_st = line.find('M',data_st_ind) + 2
        queue_space_en = line.find('~',queue_space_st)
        queue_space = int(line[queue_space_st:queue_space_en])
        queue_empty_st = line.find('A',queue_space_en) + 2
        queue_empty_en = line.find('~',queue_empty_st)
        queue_empty = int(line[queue_empty_st:queue_empty_en])
        queue_occupied_st = line.find('C',queue_empty_en) + 2
        queue_occupied_en = line.find(')',queue_occupied_st)
        queue_occupied = int(line[queue_occupied_st:queue_occupied_en])

        queue_data_st = line.find(':',queue_occupied_en)
        queue_data_en = line.find(';',queue_data_st)
        i = queue_data_st + 1
        queue_data = []
        while True:
            if line[i]==';':
                break
            if line[i]==',':
                queue_data.append('NaN')
                i+=1
            else:
                data_en = line.find(' ',i)
                cur_data = int(line[i:data_en])
                queue_data.append(cur_data)
                i = data_en + 1
        
        #write a check function if entries consistent with the data in queue
        curr_cyc_data.append(queue_data)
    cyc_data.append(curr_cyc_data)

print(cyc_data)
            




