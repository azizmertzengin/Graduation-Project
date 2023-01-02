package com.iwal.checknotifications;

import android.content.Context;
import android.os.Bundle;
import android.os.Debug;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.util.Log;

import androidx.core.app.NotificationManagerCompat;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class NotificationService extends NotificationListenerService
{
    Context context;
    OkHttpClient client = new OkHttpClient();
    String buyTemp = "";
    String apiToken = "";
    String telegramChatID = "";

    @Override
    public void onCreate()
    {
        Log.d("Sistem: ", "Aktif");
        super.onCreate();
        context = getApplicationContext();
        NotificationManagerCompat.from(context).cancelAll();
    }

    @Override
    public void onNotificationPosted(StatusBarNotification sbn)
    {
        String telegramUrl = "https://api.telegram.org/bot" + apiToken + "/sendMessage?chat_id=" + telegramChatID + "&text=";
        String sqlUrl = "https://ngtcraft.store/cryptoBot/coinEkle.php?coinName=";
        String pack = sbn.getPackageName();
        String title = "";
        String text = "";

        if (pack.equals("com.zyncas.signals"))
        //if (pack.equals("org.telegram.messenger"))
        //if (pack.equals("org.thunderdog.challegram"))
        {
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT)
            {
                Bundle extras = extras = sbn.getNotification().extras;
                title = extras.getString("android.title"); //BILDIRIMDEKI UST KISIM
                text = extras.getCharSequence("android.text").toString(); //BILDIRIMDEKI ALT KISIM
            }

            if (text.contains("New signal available"))
            {
                String[] splitText = title.split(" ");
                if (!buyTemp.equals(splitText[1]))
                {
                    buyTemp = splitText[1];
                    sqlUrl += "'" + splitText[1] + "'";
                    telegramUrl += splitText[1];
                    NotificationManagerCompat.from(context).cancelAll();
                    Request request = new Request.Builder().url(sqlUrl).build();
                    client.newCall(request).enqueue(new Callback() {
                        @Override
                        public void onFailure(Call call, IOException e) {

                        }

                        @Override
                        public void onResponse(Call call, Response response) throws IOException {

                        }
                    });




                    Request request2 = new Request.Builder().url(telegramUrl).build();
                    client.newCall(request2).enqueue(new Callback() {
                        @Override
                        public void onFailure(Call call, IOException e) {

                        }

                        @Override
                        public void onResponse(Call call, Response response) throws IOException {

                        }
                    });






                    Log.d("Package", pack);
                    Log.i("Title" , title);
                    Log.i("Text", text);
                }
            }
            /*try {
                Thread.sleep(2000);                 //1000 milliseconds is one second.
            } catch(InterruptedException ex) {
                Thread.currentThread().interrupt();
            }*/
        }



        else{
            Log.d("Uyari", "Baska bildirim geldi");
            Log.d("Package", pack);
        }
    }

    @Override
    public void onNotificationRemoved(StatusBarNotification sbn)
    {
        Log.d("Msg","Notification was removed");
    }
}