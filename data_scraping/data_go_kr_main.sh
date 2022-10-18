### python test1.py --start_point $1 --end_point $2
# shell script를 통해서 300개씩 반복하여 나눠서 start_point와 end_point를 argparse로 넘기기
for ((i = 0; i < 55148; i += 300))
    do 
        python data_go_kr_main.py --start_point $i --end_point $(( $i+300 ))
        sleep 10
    done