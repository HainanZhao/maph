\\ Exact same-character-packet alignment for one B/C overlap.
\\ Caller defines CASE_ID,D_VALUE,H11,H12,H21,H22,C_PACKET_INDEX.
default(parisizemax,4000000000);

field_polynomial(d)=
{
  if(d%4==1,return(y^2-y+(1-d)/4),return(y^2-d))
};
decode_element(code,cyc)=
{
  my(answer=vector(#cyc),q=code);
  for(index=1,#cyc,
    answer[index]=q%cyc[index];q=q\cyc[index]);
  answer
};
character_order(character,cyc)=
{
  my(answer=1);
  for(index=1,#cyc,
    answer=lcm(answer,
      cyc[index]/gcd(cyc[index],character[index])));
  answer
};
pairing(character,element,cyc)=
{
  sum(index=1,#cyc,
    character[index]*element[index]/cyc[index])
};
kernel_hnf(character,cyc)=
{
  my(elements=List(),total=vecprod(Vec(cyc)));
  for(code=0,total-1,
    my(element=decode_element(code,cyc));
    if(denominator(pairing(character,element,cyc))==1,
      listput(elements,element)));
  elements=Vec(elements);
  mathnf(concat(matdiagonal(cyc),matrix(
    #cyc,#elements,row,column,elements[column][row])))
};
same_matrix(a,b)=Str(a)==Str(b);

run_alignment() =
{
  my(Kpol=field_polynomial(D_VALUE),K=bnfinit(Kpol,1));
  my(finite=[H11,H12;H21,H22],modulus=[finite,[1,0]]);
  my(ray=bnrinit(K,modulus,1),cyc=Vec(ray.cyc));
  my(sign_generator=if(H11<=2,1,H11-1));
  my(sign_log=Vec(bnrisprincipal(
    ray,idealhnf(K,sign_generator),0)));
  my(kernels=List(),representatives=List());
  for(code=0,vecprod(cyc)-1,
    my(character=decode_element(code,cyc));
    if(character_order(character,cyc)==4
      &&denominator(pairing(character,sign_log,cyc))!=1,
      my(kernel=kernel_hnf(character,cyc),seen=0);
      for(index=1,#kernels,
        if(same_matrix(kernels[index],kernel),seen=1));
      if(!seen,
        listput(kernels,kernel);
        listput(representatives,character))
    )
  );
  kernels=Vec(kernels);representatives=Vec(representatives);
  if(C_PACKET_INDEX<1||C_PACKET_INDEX>#kernels,
    error("C packet index outside exact kernel list"));
  my(c_character=representatives[C_PACKET_INDEX]);
  my(c_kernel=kernels[C_PACKET_INDEX]);
  my(b_characters=List(),b_kernels=List());
  for(code=0,vecprod(cyc)-1,
    my(character=decode_element(code,cyc));
    if(character_order(character,cyc)==4
      &&denominator(pairing(character,sign_log,cyc))!=1,
      my(kernel=kernel_hnf(character,cyc));
      if(same_matrix(kernel,c_kernel),
        listput(b_characters,character);
        listput(b_kernels,kernel))
    )
  );
  b_characters=Vec(b_characters);b_kernels=Vec(b_kernels);
  if(#b_characters!=2,error("B projector pair count is not two"));
  if(!setsearch(Set(b_characters),c_character),
    error("C character missing from B projector"));
  my(inverse=vector(#cyc,index,
    (-c_character[index])%cyc[index]));
  if(!setsearch(Set(b_characters),inverse),
    error("C inverse missing from B projector"));
  my(c_relative=bnrclassfield(ray,c_kernel,1));
  my(b_relative=bnrclassfield(ray,b_kernels[1],1));
  my(c_absolute=rnfpolredbest(K,c_relative,2));
  my(b_absolute=rnfpolredbest(K,b_relative,2));
  if(c_relative!=b_relative,error("relative packet polynomial mismatch"));
  if(c_absolute!=b_absolute,error("absolute packet polynomial mismatch"));

  print("CASE_ID=",CASE_ID);
  print("FINITE_IDEAL=",finite);
  print("INFINITE_COMPONENT=",modulus[2]);
  print("RAY_STRUCTURE=",cyc);
  print("SIGN_LOG=",sign_log);
  print("C_PACKET_INDEX=",C_PACKET_INDEX);
  print("C_CHARACTER=",c_character);
  print("C_INVERSE_CHARACTER=",inverse);
  print("C_KERNEL_HNF=",c_kernel);
  print("B_PROJECTOR_CHARACTERS=",b_characters);
  print("C_PACKET_RELATIVE_POLYNOMIAL=",c_relative);
  print("B_PACKET_RELATIVE_POLYNOMIAL=",b_relative);
  print("IDENTICAL_RELATIVE_PACKET_POLYNOMIAL=1");
  print("IDENTICAL_ABSOLUTE_PACKET_POLYNOMIAL=1");
  print("SAME_MODULUS=1");
  print("SAME_RAY_CLASSES=1");
  print("SAME_CHARACTER_PAIR=1");
  print("DUAL_PACKET_ALIGNMENT_VERIFIED=1");
  print("PROMOTION_STATE=ALIGNMENT_ONLY_NO_DUAL_PROOF")
};

run_alignment();
