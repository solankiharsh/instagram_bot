from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd

def open_chrome():
    chromedriver_path = r'C:/Users/ttreasa/Downloads/chromedriver_win32/chromedriver.exe'
    wb = webdriver.Chrome(executable_path=chromedriver_path)
    sleep(2)
    wb.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sleep(3)

    username = wb.find_element_by_name('username')
    username.send_keys('urbansanyaasii')
    password = wb.find_element_by_name('password')
    password.send_keys('YOUR_PASSWORD')
    button_login = wb.find_element_by_css_selector('#loginForm > div > div:nth-child(3) > button > div')
    button_login.click()
    sleep(3) #loginForm > div > div:nth-child(3) > button > div
    notnow = wb.find_element_by_css_selector('#react-root > section > main > div > div > div > div > button')
    notnow.click() #comment these last 2 lines out, if you don't get a pop up asking about notifications
    not_now2 = wb.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm')
    not_now2.click()
    hashtag_list = ['travel']

    prev_user_list = []
    #prev_user_list = pd.read_csv('20181203-224633_users_followed_list.csv', delimiter=',').iloc[:,
    #                 1:2]  # useful to build a user log
    #prev_user_list = list(prev_user_list['0'])

    new_followed = []
    tag = -1
    followed = 0
    likes = 0
    comments = 0

    for hashtag in hashtag_list:
        tag += 1
        wb.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
        sleep(5)
        first_thumbnail = wb.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')

        first_thumbnail.click()
        print('thumbnail clicked')
        sleep(randint(1, 2))
        try:
            for x in range(1, 200):
                username = wb.find_element_by_xpath(
                    '/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
                print('got username')
                print(username)

                if username not in prev_user_list:
                    # If we already follow, do not unfollow
                    if wb.find_element_by_xpath(
                            '/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':

                        wb.find_element_by_xpath(
                            '/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()

                        new_followed.append(username)
                        followed += 1

                        # Liking the picture
                        button_like = wb.find_element_by_xpath(
                            '/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span/svg/path')

                        button_like.click()
                        likes += 1
                        sleep(randint(18, 25))

                        # Comments and tracker
                        comm_prob = randint(1, 10)
                        print('{}_{}: {}'.format(hashtag, x, comm_prob))
                        if comm_prob > 1:
                            comments += 1
                            wb.find_element_by_xpath(
                                '/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/textarea').click()
                            comment_box = wb.find_element_by_xpath(
                                '/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/textarea')


                            if (comm_prob > 1):
                                comment_box.send_keys('Really awesome!')
                                sleep(1)
                            elif (comm_prob > 6) and (comm_prob < 9):
                                comment_box.send_keys('Great job :)')
                                sleep(1)
                            elif comm_prob == 9:
                                comment_box.send_keys('Superb gallery!! Loved it')
                                sleep(1)
                            elif comm_prob == 10:
                                comment_box.send_keys('That is dope :)')
                                sleep(1)
                            # Enter to post comment
                            comment_box.send_keys(Keys.ENTER)
                            sleep(randint(22, 28))

                    # Next picture
                    next_button = wb.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a')
                    next_button.click()
                    sleep(randint(25, 29))
        except:
            continue

    for n in range(0, len(new_followed)):
        prev_user_list.append(new_followed[n])

    updated_user_df = pd.DataFrame(prev_user_list)
    updated_user_df.to_csv('{}_users_followed_list.csv'.format(strftime("%Y%m%d-%H%M%S")))
    print('Liked {} photos.'.format(likes))
    print('Commented {} photos.'.format(comments))
    print('Followed {} new people.'.format(followed))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    open_chrome()



