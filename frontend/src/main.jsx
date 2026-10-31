import React,{useEffect,useState} from 'react';import{createRoot}from'react-dom/client';import{Landmark,Search,UserRound,ShieldCheck,Bookmark,ArrowRight,LogOut,CheckCircle2,AlertCircle}from'lucide-react';import './style.css';
function App(){const[token,setToken]=useState(sessionStorage.getItem('token')||'');const[mode,setMode]=useState('login');const[email,setEmail]=useState('');const[password,setPassword]=useState('');const[error,setError]=useState('');const[page,setPage]=useState('discover');const[schemes,setSchemes]=useState([]);const[results,setResults]=useState(null);const[query,setQuery]=useState('');const[profile,setProfile]=useState({age:'',state:'Madhya Pradesh',occupation:'',annual_income:'',interests:''});const[busy,setBusy]=useState(false);
const [savedSchemes, setSavedSchemes] = useState([]);
async function api(path, options = {}) {
  const res = await fetch('/api' + path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: 'Bearer ' + token } : {}),
      ...(options.headers || {})
    }
  });

  const data = await res.json();

  if (res.status === 401 && path !== '/auth/login') {
    sessionStorage.removeItem('token');
    setToken('');
    setResults(null);
    setError('Your session has expired. Please sign in again.');
    throw new Error('Your session has expired. Please sign in again.');
  }

  if (!res.ok) {
    throw new Error(data.error || data.msg || 'Request failed');
  }

  return data;
}

useEffect(()=>{api('/schemes').then(setSchemes).catch(e=>setError(e.message));},[]);
useEffect(()=>{if(token)api('/profile').then(p=>setProfile(Object.fromEntries(Object.entries(p).map(([k,v])=>[k,v??''])))).catch(()=>{});},[token]);
async function auth(e){e.preventDefault();setError('');setBusy(true);try{if(mode==='register'){await api('/auth/register',{method:'POST',body:JSON.stringify({email,password})});setMode('login');setError('Account created. Sign in now.');}else{const r=await api('/auth/login',{method:'POST',body:JSON.stringify({email,password})});sessionStorage.setItem('token',r.access_token);setToken(r.access_token);}}catch(e){setError(e.message)}finally{setBusy(false)}}
async function saveProfile(e){e.preventDefault();setBusy(true);setError('');try{const p={...profile,age:profile.age===''?null:Number(profile.age),annual_income:profile.annual_income===''?null:Number(profile.annual_income)};setProfile(await api('/profile',{method:'PUT',body:JSON.stringify(p)}));setPage('discover')}catch(e){setError(e.message)}finally{setBusy(false)}}
async function recommend(e){e.preventDefault();setBusy(true);setError('');try{setResults(await api('/recommendations',{method:'POST',body:JSON.stringify({query})}))}catch(e){setError(e.message)}finally{setBusy(false)}}
async function bookmark(id){try{await api('/saved',{method:'POST',body:JSON.stringify({scheme_id:id})});setError('Scheme saved to your account.')}catch(e){setError(e.message)}}
return <><header><div className="brand"><div className="brandicon"><Landmark size={22}/></div><div>JanSetu <span>AI</span><small>Government Scheme Assistant</small></div></div><nav><button className={page==='discover'?'selected':''} onClick={()=>setPage('discover')}>Discover</button><button className={page==='profile'?'selected':''} onClick={()=>setPage('profile')}>My Profile</button>{token&&<button onClick={()=>{sessionStorage.removeItem('token');setToken('');setResults(null)}}><LogOut size={16}/> Sign out</button>}
<button
  className={page === 'saved' ? 'selected' : ''}
  onClick={async () => {
    setError('');
    try {
      const data = await api('/saved');
      setSavedSchemes(data);
      setPage('saved');
    } catch (e) {
      setError(e.message);
    }
  }}
>
  <Bookmark size={16} /> My Saved Schemes
</button>
</nav></header><main><section className="hero"><div className="eyebrow"><ShieldCheck size={15}/> CITIZEN-CENTRIC AI ASSISTANCE</div><h1>Government support,<br/><em>made easier to discover.</em></h1><p>Find relevant schemes, understand recorded eligibility conditions, and follow official application guidance — with clear explanations and source transparency.</p><div className="hero-tags"><span>Personalized discovery</span><span>Explainable screening</span><span>Official source links</span></div></section>{error&&<div className="notice"><AlertCircle size={17}/>{error}<button onClick={()=>setError('')}>×</button></div>}{!token?<section className="auth"><div><div className="sectiontag">GET STARTED</div><h2>Your bridge to better access</h2><p>Create a profile to receive personalized scheme rankings. No government ID is required to explore this prototype.</p><div className="benefit"><CheckCircle2 size={18}/> Privacy-conscious profile fields</div><div className="benefit"><CheckCircle2 size={18}/> Clear reasons behind screening outcomes</div></div><form onSubmit={auth} className="panel"><h3>{mode==='login'?'Welcome back':'Create your account'}</h3><label>Email address<input type="email" value={email} onChange={e=>setEmail(e.target.value)} required placeholder="you@example.com"/></label><label>Password<input type="password" minLength={10} value={password} onChange={e=>setPassword(e.target.value)} required placeholder="At least 10 characters"/></label><button className="primary" disabled={busy}>{mode==='login'?'Sign in':'Create account'} <ArrowRight size={17}/></button><p className="small">{mode==='login'?"Don't have an account? ":'Already registered? '}<button type="button" className="textbtn" onClick={()=>setMode(mode==='login'?'register':'login')}>{mode==='login'?'Register':'Sign in'}</button></p></form></section>
:page==='saved'?
<section className="workspace">
  <div className="sectiontag">
    <Bookmark size={16}/> SAVED SCHEMES
  </div>

  <h2>My Saved Schemes</h2>
  <p>Government schemes you have bookmarked for later.</p>

  {savedSchemes.length === 0 ? (
    <div className="empty">
      <Bookmark size={36}/>
      <h3>No saved schemes yet</h3>
      <p>Visit Discover and save a scheme to see it here.</p>
    </div>
  ) : (
    <div className="cards">
      {savedSchemes.map(s => (
        <article className="scheme" key={s.id}>
          <div className="scheme-top">
            <span className="category">{s.category}</span>
          </div>

          <h3>{s.name}</h3>
          <p>{s.description}</p>

          <div className="scheme-actions">
            <a
              href={s.official_url}
              target="_blank"
              rel="noopener noreferrer"
            >
              Official source <ArrowRight size={15}/>
            </a>
          </div>
        </article>
      ))}
    </div>
  )}
</section>
:page==='profile'?
<section className="workspace"><div className="sectiontag"><UserRound size={16}/> CITIZEN PROFILE</div><h2>Your details</h2><p>Only enter information you are comfortable sharing. Blank values remain unknown during eligibility screening.</p><form className="panel profileform" onSubmit={saveProfile}><label>Age<input type="number" min="0" max="120" value={profile.age} onChange={e=>setProfile({...profile,age:e.target.value})}/></label><label>State<input value={profile.state} onChange={e=>setProfile({...profile,state:e.target.value})}/></label><label>Occupation<input value={profile.occupation} onChange={e=>setProfile({...profile,occupation:e.target.value})}/></label><label>Annual family income (₹)<input type="number" min="0" value={profile.annual_income} onChange={e=>setProfile({...profile,annual_income:e.target.value})}/></label><label className="wide">Interests and needs<input value={profile.interests} onChange={e=>setProfile({...profile,interests:e.target.value})} placeholder="Education, farming, entrepreneurship..."/></label><button className="primary" disabled={busy}>Save profile <ArrowRight size={16}/></button></form></section>:<section className="workspace"><div className="sectiontag"><Search size={16}/> SCHEME DISCOVERY</div><h2>Explore schemes for you</h2><p>Recommendations are relevance rankings, not official approval or proof of eligibility.</p><form className="searchbar" onSubmit={recommend}><Search size={20}/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Try: education scholarship, farming, business support..."/><button className="primary" disabled={busy}>Find schemes <ArrowRight size={16}/></button></form><div className="sectionrow"><h3>{results?'Personalized recommendations':'Published government schemes'}</h3><span>{(results||schemes).length} results</span></div>{(results||schemes).length===0?<div className="empty"><Landmark size={36}/><h3>No government schemes published yet</h3><p>The administrator must add official source-verified schemes and current eligibility rules. This prototype deliberately does not invent scheme requirements.</p></div>:<div className="cards">{(results||schemes).map(s=><article className="scheme" key={s.id}><div className="scheme-top"><span className="category">{s.category}</span>{s.relevance_score!==undefined&&<span className="score">Relevance {Math.round(s.relevance_score*100)}%</span>}</div><h3>{s.name}</h3><p>{s.description}</p>{s.eligibility&&<div className="status">Screening: {s.eligibility.status.replaceAll('_',' ')}
<small>
  {s.eligibility.checks.map(c => {
    const field = c.field.replaceAll('_', ' ');
    const explanation =
      c.result === 'unknown'
        ? (c.reason || 'Manual verification required')
        : c.result === 'pass'
          ? 'Recorded condition satisfied'
          : 'Recorded condition not satisfied';

    return `${field}: ${explanation}`;
  }).join(' · ')}
</small>
</div>}<div className="scheme-actions"><a href={s.official_url} target="_blank" rel="noopener noreferrer">Official source <ArrowRight size={15}/></a><button onClick={()=>bookmark(s.id)}><Bookmark size={16}/> Save</button></div></article>)}</div>}</section>}</main><footer><div className="brand"><Landmark size={20}/> JanSetu AI</div><p>Academic prototype. Not affiliated with or endorsed by any government. Verify all decisions on official portals.</p></footer></>}
createRoot(document.getElementById('root')).render(<App/>);
