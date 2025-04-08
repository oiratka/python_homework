#Task 1: Diary
import traceback

try:
    with open ("diary.txt", "a") as diary_file:
         prompt_entry = input ("What happened today?")
         
         while prompt_entry.lower() != "done for now":
            diary_file.write(prompt_entry + "\n")
            prompt_entry = input ("What else?")
            diary_file.write("done for now\n")
            print("End of diary")

except Exception as e:
   trace_back = traceback.extract_tb(e.__traceback__)
   stack_trace = list()
   for trace in trace_back:
      stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
   print(f"Exception type: {type(e).__name__}")
   message = str(e)
   if message:
      print(f"Exception message: {message}")
   print(f"Stack trace: {stack_trace}")

  
