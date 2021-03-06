package aditi.ayush.nikhil.complaintmanagement;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.design.widget.NavigationView;
import android.support.design.widget.TabLayout;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.GravityCompat;
import android.support.v4.view.ViewPager;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.common.api.GoogleApiClient;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class Admin_complaints extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    home home = new home();
    MyApp_cookie cook = new MyApp_cookie();
    resolved resolved = new resolved();
    unresolved unresolved = new unresolved();
    for_resolution for_res=new for_resolution();

    /**
     * ATTENTION: This was auto-generated to implement the App Indexing API.
     * See https://g.co/AppIndexing/AndroidStudio for more information.
     */
    private GoogleApiClient client;
    private Toolbar toolbar;
    private TabLayout tabLayout;
    private ViewPager viewPager;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_complaint_page);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

     /*   Bundle registrationData = getIntent().getExtras();
        if(registrationData == null){
            return;
        }

        String UserType = registrationData.getString("UserType");
*/
      /*  FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
    */
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        viewPager = (ViewPager) findViewById(R.id.viewpager);
        setupViewPager(viewPager, "abc");

        tabLayout = (TabLayout) findViewById(R.id.tabs);
        tabLayout.setupWithViewPager(viewPager);
        boolean Active=true;
        String activetab="0";
        if (Active) {
            viewPager.setCurrentItem(Integer.parseInt(activetab));
        }
//TODO: set visibilities of user depending on user type

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        String url=getResources().getString(R.string.IP)+"/admin_complaint/get_all_complaints.json";



        final ArrayList<String> res_content=new ArrayList<String>();
        final ArrayList<String> unres_content=new ArrayList<String>();
        final ArrayList<String> markedforres_content=new ArrayList<String>();
        final ArrayList<String> res_id=new ArrayList<String>();
        final ArrayList<String> unres_id=new ArrayList<String>();
        final ArrayList<String> markedforres_id=new ArrayList<String>();
        final ArrayList<String> res_type=new ArrayList<String>();
        final ArrayList<String> unres_type=new ArrayList<String>();
        final ArrayList<String> markedforres_type=new ArrayList<String>();

        //TODO: Call the api's to get concerned complaint list and notifications and populate in this only
        StringRequest cpass = new StringRequest (Request.Method.GET, url,
                new Response.Listener<String>()
                {
                    @Override
                    public void onResponse(String response)
                    {
                        Log.i("yo", "why this ... working" + response);
///                        System.out.println(response.toString());
//                        Toast.makeText(getActivity().getApplicationContext(),
//                                "Logout ",
//                                Toast.LENGTH_LONG).show();
                        try
                        { System.out.println("finally yup");
                            JSONObject json_data = new JSONObject(response);
                            boolean succ = json_data.getBoolean("success");
                            if (succ)
                            {
                                JSONArray array_ind=json_data.getJSONArray("Individual");
                                JSONArray array_hos=json_data.getJSONArray("Hostel");
                                JSONArray array_insti=json_data.getJSONArray("inst_comp");

                                for(int i=0;i<array_ind.length();i++)
                                {
                                JSONObject json_ob=array_ind.getJSONObject(i);
                                String content=json_ob.getString("compaint_content");
                                String id=json_ob.getString("complaint_id");
                                int i_res=json_ob.getInt("resolved");

                                    int i_markres=json_ob.getInt("mark_for_resolution");
                                if(i_res==1)
                                {
                                    res_content.add(content);
                                    res_id.add(id);
                                    res_type.add("1");
                                }
                                else if(i_res==0 && i_markres == 0)
                                {
                                    unres_content.add(content);
                                    unres_id.add(id);
                                    unres_type.add("1");
                                }
                                else  {
//                                    ires = 0, marked = 1
                                    markedforres_content.add(content);
                                    markedforres_id.add(id);
                                    markedforres_type.add("1");
                                }
                                }
                                for(int i=0;i<array_hos.length();i++)
                                {JSONObject json_ob=array_hos.getJSONObject(i);
                                    String content=json_ob.getString("compaint_content");
                                    String id=json_ob.getString("complaint_id");
                                    int i_res=json_ob.getInt("resolved");
                                    int i_markres=json_ob.getInt("mark_for_resolution");
                                    if(i_res==1)
                                    {
                                        res_content.add(content);
                                        res_id.add(id);
                                        res_type.add("2");
                                    }
                                    else if(i_res==0 && i_markres == 0)
                                    {
                                        unres_content.add(content);
                                        unres_id.add(id);
                                        unres_type.add("2");
                                    }
                                    else {
                                        markedforres_content.add(content);
                                        markedforres_id.add(id);
                                        markedforres_type.add("2");
                                    }

                                }
                                for(int i=0;i<array_insti.length();i++)
                                {
                                    JSONObject json_ob=array_insti.getJSONObject(i);
                                    String content=json_ob.getString("compaint_content");
                                    String id=json_ob.getString("complaint_id");
                                    int i_res=json_ob.getInt("resolved");
                                    int i_markres=json_ob.getInt("mark_for_resolution");
                                    if(i_res==1)
                                    {
                                        res_content.add(content);
                                        res_id.add(id);
                                        res_type.add("3");
                                    }
                                    else if(i_res==0 && i_markres == 0)
                                    {
                                        unres_content.add(content);
                                        unres_id.add(id);
                                        unres_type.add("3");
                                    }
                                    else {
                                        markedforres_content.add(content);
                                        markedforres_id.add(id);
                                        markedforres_type.add("3");
                                    }

                                }

                                Bundle bund1=new Bundle();
                                bund1.putStringArrayList("content",res_content);
                                bund1.putStringArrayList("id",res_id);
                                bund1.putStringArrayList("type",res_type);
                                // bund1.p

                                resolved.setArguments(bund1);
                                Bundle bund2=new Bundle();
                                bund1.putStringArrayList("content",unres_content);
                                bund1.putStringArrayList("id",unres_id);
                                bund1.putStringArrayList("type",unres_type);

                                unresolved.setArguments(bund2);
                                Bundle bund3=new Bundle();
                                bund1.putStringArrayList("content",markedforres_content);
                                bund1.putStringArrayList("id",markedforres_id);
                                bund1.putStringArrayList("type",markedforres_type);
                                for_res.setArguments(bund3);



                            }


                        } catch (Exception e)
                        {
                            e.printStackTrace();
                            Toast.makeText(getApplicationContext(),
                                    "Error: " + e.getMessage(),
                                    Toast.LENGTH_LONG).show();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.i("yo", "why this not working");
                        //  Toast.makeText(getActivity().getApplicationContext(), error.toString(), Toast.LENGTH_LONG).show();
                    }
                });
        Volley.newRequestQueue(getApplicationContext()).add(cpass);


/*

        Bundle bund1=new Bundle();
       bund1.putStringArrayList("content",res_content);
       bund1.putStringArrayList("id",res_id);
       bund1.putStringArrayList("type",res_type);
       // bund1.p

       resolved.setArguments(bund1);
        Bundle bund2=new Bundle();
        bund1.putStringArrayList("content",unres_content);
        bund1.putStringArrayList("id",unres_id);
        bund1.putStringArrayList("type",unres_type);

        unresolved.setArguments(bund2);
        Bundle bund3=new Bundle();
        bund1.putStringArrayList("content",markedforres_content);
        bund1.putStringArrayList("id",markedforres_id);
        bund1.putStringArrayList("type",markedforres_type);
        for_res.setArguments(bund3);
*/








//        pop_complaint_list();//These function can be shifted to their respective fragments as well
//        pop_noti_list();
        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client = new GoogleApiClient.Builder(this).addApi(AppIndex.API).build();
    }
    private void setupViewPager(ViewPager viewPager, String User)
    {/** Adding Fragments  to the Tab View **/
        ViewPagerAdapter adapter = new ViewPagerAdapter(getSupportFragmentManager());
       /* if(User.equals("Special")){
            adapter.addFragment(home, "Home");}*/
        adapter.addFragment(unresolved, "Unresolved");
        adapter.addFragment(for_res, "Marked For Resolution");
        adapter.addFragment(resolved, "Resolved");
        viewPager.setAdapter(adapter);
    }

    //    public void Reg_comp(View view)
//    {
//        TextView txt=(TextView) findViewById(R.id.Reg);
//        txt.setText("Hello clickable");
//        //TODO: Add an intent to open a new Activity to  Register a Complaint
//
//
//    }
//    public void My_Complaints(View view)
//    {
//        TextView txt=(TextView) findViewById(R.id.My_comp);
//        txt.setText("Hello clickable");
//        String url="http://127.0.0.1/admin_complaint/get_all_complaints.json";
//        JsonObjectRequest stringRequest = new JsonObjectRequest(Request.Method.GET, url, null,
//                new Response.Listener<JSONObject>() {
//                    @Override
//                    public void onResponse(JSONObject response)
//                    {
//                        //TODO: Add an intent to open a new Activity showing self registered complaints or add it as a tab
//                    }
//                },
//                new Response.ErrorListener() {
//                    @Override
//                    public void onErrorResponse(VolleyError error) {
//                        Toast.makeText(HomePage.this, error.toString(), Toast.LENGTH_LONG).show();
//                    }
//                });
//
//        Volley.newRequestQueue(this).add(stringRequest);
//
//    }
//    public void Add_User(View view)
//    {
//        TextView txt=(TextView) findViewById(R.id.Add_User);
//        txt.setText("Hello clickable");
//        Intent I=new Intent(HomePage.this,addUser.class);
//        startActivity(I);
//    }
//    public void pop_complaint_list()
//    {String url= "http://127.0.0.1/complaint_data/get_all.json";
//        JsonObjectRequest stringRequest = new JsonObjectRequest(Request.Method.GET, url, null,
//                new Response.Listener<JSONObject>() {
//                    @Override
//                    public void onResponse(JSONObject response)
//                    {//TODO
//                        //We receive a set of complaints..sort them on the basis of level
//                        // make array on the basis of response array and populate the list view
//
//                    }
//                },
//                new Response.ErrorListener() {
//                    @Override
//                    public void onErrorResponse(VolleyError error) {
//                        Toast.makeText(ComplaintPage.this, error.toString(), Toast.LENGTH_LONG).show();
//                    }
//                });
//
//        Volley.newRequestQueue(this).add(stringRequest);
//    }
//    public void pop_noti_list()
//    {String url= "http://10.192.38.23:8000/notification/get_noti.json";
//        JsonObjectRequest stringRequest = new JsonObjectRequest(Request.Method.GET, url, null,
//                new Response.Listener<JSONObject>() {
//                    @Override
//                    public void onResponse(JSONObject response)
//                    {//TODO
//                        //We receive a set of complaints..sort them on the basis of level
//                        // make array on the basis of response array and populate the list view
//
//                    }
//                },
//                new Response.ErrorListener() {
//                    @Override
//                    public void onErrorResponse(VolleyError error) {
//                        Toast.makeText(ComplaintPage.this, error.toString(), Toast.LENGTH_LONG).show();
//                    }
//                });
//
//        Volley.newRequestQueue(this).add(stringRequest);
//    }
    @Override
    public void onStart() {
        super.onStart();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client.connect();
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "HomePage Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app deep link URI is correct.
                Uri.parse("android-app://aditi.ayush.nikhil.complaintmanagement/http/host/path")
        );
        AppIndex.AppIndexApi.start(client, viewAction);
    }

    @Override
    public void onStop() {
        super.onStop();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "HomePage Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app deep link URI is correct.
                Uri.parse("android-app://aditi.ayush.nikhil.complaintmanagement/http/host/path")
        );
        AppIndex.AppIndexApi.end(client, viewAction);
        client.disconnect();
    }

    class ViewPagerAdapter extends FragmentPagerAdapter {
        /**
         * A class to populate the Tab Views
         **/
        private final List<Fragment> mFragmentList = new ArrayList<>();
        private final List<String> mFragmentTitleList = new ArrayList<>();

        public ViewPagerAdapter(FragmentManager manager) {
            super(manager);
        }

        @Override
        public Fragment getItem(int position) {
            return mFragmentList.get(position);
        }

        @Override
        public int getCount() {
            return mFragmentList.size();
        }

        public void addFragment(Fragment fragment, String title) {
            mFragmentList.add(fragment);
            mFragmentTitleList.add(title);
        }

        @Override
        public CharSequence getPageTitle(int position) {
            return mFragmentTitleList.get(position);
        }
    }


    ///////////////////////////////Navigation Drawer Related stuff
    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.complaint_page, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_logout)
        {   String url= getResources().getString(R.string.IP) + "/default/logout.json";
            JsonObjectRequest stringRequest = new JsonObjectRequest(Request.Method.GET, url, null,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response)
                        {Intent i=new Intent(Admin_complaints.this,MainActivity.class);
                            Toast.makeText(Admin_complaints.this,"",Toast.LENGTH_SHORT).show();
                            startActivity(i);
                        }
                    },
                    new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            Toast.makeText(Admin_complaints.this, error.toString(), Toast.LENGTH_LONG).show();
                        }
                    });

            Volley.newRequestQueue(this).add(stringRequest);

            return true;
        }
        if (id == R.id.action_Change_pass)
        {//TODO: direct to a new activity or we can use popup dialog box
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.complaints) {
            // Handle the camera action
        } else if (id == R.id.Notifications)
        {

        }
        else if (id == R.id.action_Change_pass)
        { Intent i=new Intent(Admin_complaints.this,ChangePassword.class);
            startActivity(i);
        } else if (id == R.id.Set_Preferences)
        {Intent i =new Intent(Admin_complaints.this,Preferences.class);
            startActivity(i);
        } else if (id == R.id.action_logout)
        { String url= getResources().getString(R.string.IP) + "/default/logout.json";
            JsonObjectRequest stringRequest = new JsonObjectRequest(Request.Method.GET, url, null,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response)
                        {Intent i=new Intent(Admin_complaints.this,MainActivity.class);
                            Toast.makeText(Admin_complaints.this,"",Toast.LENGTH_SHORT).show();
                            startActivity(i);
                        }
                    },
                    new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            Toast.makeText(Admin_complaints.this, error.toString(), Toast.LENGTH_LONG).show();
                        }
                    });

            Volley.newRequestQueue(this).add(stringRequest);


        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }
}
